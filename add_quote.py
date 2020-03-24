while True:
    input_value=input("请输入字符串:\n")
    print(input_value)
    items=input_value.split("&")
    form_data={}
    for item in items:
        key=item.split("=")[0]
        value=item.split("=")[1]
        form_data[key]=value

    print(form_data)
    print(form_data.keys())


