def clean_task_info(task_info):
    print(task_info)
    expected_keys = [
        "task_category", "task_subcategory", "period_date",
        "task_description", "competitors_links", "goods_sku",
        "goods_info", "task_action", "task_date", "task_report_week",
        "warehouse"
    ]
    
    default_value = "-"
    default_int_value = 0

    

    if not isinstance(task_info, dict):
        task_info = {}
    
    for key in expected_keys:
        task_info[key] = task_info.get(key) or default_value
    
    print(task_info)
    return task_info