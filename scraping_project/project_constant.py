SCRAP_USERS = {
    "status": {
        "APPROVED": 1,
        "PENDING":  2,
        "REJECTED": 3
    },
    "roles": {
        1: "SUPER ADMIN",
        2: "ADMIN",
        3: "USER"
    }
}


PAGINATION_CONSTANT = {
    "page_size":10,
    "max_page_size": 100,
    "page_size_query_param": 'page_size'
}



DIRECTORY = {
    "user_authentication":{
        "profile_pic": "app_auth/profile/" 
    }
}
