import time
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from orchestrator_core import run_workflow, load_agent
from datetime import datetime, timedelta
import os

CONFIG_SCHEDULE_PATH = "configs/workflow_schedules.yaml"
CONFIG_ALERT_PATH = "configs/alert_rules.yaml"
ALERT_HISTORY_PATH = "logs/alert_history.log"
CRON_HISTORY_PATH = "logs/cron_history.log"

alert_last_triggered = {}


def load_schedules():
    if not os.path.exists(CONFIG_SCHEDULE_PATH):
        return []
    with open(CONFIG_SCHEDULE_PATH) as f:
        data = yaml.safe_load(f) or {}
    return data.get("schedules", [])


def load_alerts():
    if not os.path.exists(CONFIG_ALERT_PATH):
        return []
    with open(CONFIG_ALERT_PATH) as f:
        data = yaml.safe_load(f) or {}
    return data.get("alerts", [])


def resolve_env_vars(input_dict):
    for k, v in input_dict.items():
        if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
            env_key = v[2:-1]
            input_dict[k] = os.getenv(env_key, v)
    return input_dict


def log_alert(name, message):
    os.makedirs(os.path.dirname(ALERT_HISTORY_PATH), exist_ok=True)
    with open(ALERT_HISTORY_PATH, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {name}: {message}\n")


def log_cron(name, message):
    os.makedirs(os.path.dirname(CRON_HISTORY_PATH), exist_ok=True)
    with open(CRON_HISTORY_PATH, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {name}: {message}\n")


def schedule_jobs(scheduler):
    schedules = load_schedules()
    for job in schedules:
        name = job["name"]
        cron_expr = job["cron"].split()
        workflow = job["workflow"]

        if len(cron_expr) != 5:
            print(f"❌ Invalid cron expression for job {name}")
            continue

        minute, hour, day, month, weekday = cron_expr

        def job_fn(path=workflow, job_name=name):
            print(f"\n⏰ Running scheduled job: {job_name} at {datetime.now()}")
            log_cron(job_name, "Started")
            try:
                run_workflow(path)
                log_cron(job_name, "Completed successfully")
            except Exception as e:
                print(f"❌ Failed to run workflow {path}: {e}")
                log_cron(job_name, f"Error: {e}")

        scheduler.add_job(job_fn, 'cron', id=name, minute=minute, hour=hour, day=day, month=month, day_of_week=weekday)


def schedule_alerts(scheduler):
    alerts = load_alerts()

    for alert in alerts:
        name = alert["name"]
        condition = alert["condition"]
        interval = int(alert["interval"])
        actions = alert.get("actions", [])
        cooldown = alert.get("cooldown", 300)

        def check_alert(name=name, condition=condition, actions=actions, cooldown=cooldown):
            print(f"🔍 Evaluating alert: {name}")
            try:
                now = datetime.now()
                last_time = alert_last_triggered.get(name)
                if last_time and now - last_time < timedelta(seconds=cooldown):
                    print(f"⏱️ Cooldown active for alert '{name}'")
                    return

                if eval(condition):
                    print(f"\n🚨 Alert triggered: {name} at {now}")
                    log_alert(name, "Triggered")
                    alert_last_triggered[name] = now
                    for action in actions:
                        print(f"  → Execute action: {action}")
                        agent_name = action.get("agent")
                        if not agent_name:
                            print("⚠️ Missing agent in action.")
                            continue
                        try:
                            agent = load_agent(agent_name)
                            resolved_input = resolve_env_vars(action.get("input", {}))
                            result = agent.run(**resolved_input)
                            print(f"    ✅ Action result: {result}")
                        except Exception as e:
                            print(f"    ❌ Failed to execute agent '{agent_name}': {e}")
                            log_alert(name, f"Error: {e}")
            except Exception as e:
                print(f"❌ Error evaluating alert {name}: {e}")
                log_alert(name, f"Error: {e}")

        scheduler.add_job(check_alert, 'interval', seconds=interval, id=f"alert_{name}")


def main():
    scheduler = BackgroundScheduler()
    schedule_jobs(scheduler)
    schedule_alerts(scheduler)
    scheduler.start()
    print("✅ Scheduler started. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Scheduler stopped.")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
