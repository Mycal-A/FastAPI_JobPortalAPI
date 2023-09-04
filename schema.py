def individual_serial(user_reg) -> dict:
    return {
        "id": str(user_reg["_id"]),
        "name": user_reg["name"],
        "role": user_reg["role"],
        "email": user_reg["email"],
        "location": user_reg["location"],
        "phone": user_reg["phone"],
        "password": user_reg["password"]
    }


def list_serial(todos) -> list:
    return [individual_serial(user_reg) for user_reg in todos]

# for getting job post details


def individual_adminserial(job_post) -> dict:
    return {
        "jobid": str(job_post["jobid"]),
        "title": job_post["title"],
        "description": job_post["description"],
        "salary": job_post["salary"]
    }


def list_admin_serial(todos) -> list:
    return [individual_adminserial(job_post) for job_post in todos]

# for the user to view job posts


def individual_user_serial(job_post) -> dict:
    return {
        "jobid": str(job_post["jobid"]),
        "title": job_post["title"],
        "description": job_post["description"],
        "salary": job_post["salary"]
    }


def list_user_serial(job_posts) -> list:
    return [individual_user_serial(job_post) for job_post in job_posts]


# For getting job applies details
def individual_jobserial(view_applies) -> dict:
    if isinstance(view_applies, dict):
        jobid = view_applies.get("jobid")
        email = view_applies.get("email", [])
    else:
        jobid = None
        email = []

    return {
        "jobid": jobid,
        "email": email  # Keep as a list
    }


def list_job_serial(todos) -> list:
    return [individual_jobserial(view_applies) for view_applies in todos if isinstance(view_applies, dict)]


# def individual_jobserial(view_applies) -> dict:
#     if "jobid" in view_applies:
#         jobid = view_applies["jobid"]
#     else:
#         jobid = None  # Handle the case when "jobid" is missing

#     return {
#         "jobid": jobid,
#         "email": view_applies.get("email", [])  # Keep as a list
#     }


# def list_job_serial(todos) -> list:
#     return [individual_jobserial(view_applies) for view_applies in todos]
