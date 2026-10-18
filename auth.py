from database import run_query


def _table_for_role(role):
    return {"manager": "managers", "student": "students"}.get(role.lower())


def register(role, username, password, name=False):
    table = _table_for_role(role)
    if table is None:
        return {
            "success": False,
            "message": f"[ERROR]: Unsupported role: {role}"
        }

    try:
        run_query(
            f"INSERT INTO {table}(name, username, password) VALUES(%s, %s, %s)",
            (name, username, password)
        )
    except Exception as e:
        return {
            "success": False,
            "message": f"[ERROR]: {e}"
        }
    else:
        return {
            "success": True,
            "message": f"{role} user created successfully"
        }


def login(role, username, password):
    table = _table_for_role(role)
    if table is None:
        return {
            "success": False,
            "message": f"[ERROR]: Unsupported role: {role}"
        }

    try:
        res = run_query(
            f"SELECT * FROM {table} WHERE username=%s AND password=%s",
            (username, password),
            fetch=True
        )

        if res:
            name = res[0][1]
            msg = f"Welcome {name}!"
        else:
            return {
                "success": False,
                "message": f"No {role.lower()}s record found"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"[ERROR]: {e}"
        }
    else:
        return {
            "success": True,
            "message": msg,
            "data": res[0]
        }
