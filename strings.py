start_cmd_string = 'Я Servus Systems Integration бот! \n' \
                   'Я допомагатиму Вам в нескладних питаннях, таких як:\n' \
                   '- замовлення 📄 паперу для терміналу\n' \
                   '- замовлення зворотного дзівнка\n' \
                   '- виклик майстра для усунення технічних несправностей'

pos_photo_string = 'Для початку введіть серійний номер терміналу! \n' \
                   'Серійний номер знаходиться на зворотній стороні терміналу після напису S/N як показано на фото ' \
                   'вище, але без «-» та відступів.\n' \
                   'Приклад: 123456789 або VN000000.'

icon_true = '✅'
icon_true2 = '✔'
icon_crossmark = '❌'
icon_no = '⛔'
choice_string = 'Оберіть: \n'
order_call_string = 'Для замовлення зворотного дзвінка введіть номер телефону\n'
order_call_string_after = 'Замовлення, недовзы з вами звяжуться наші менеджери \n'
order_paper_string = 'Для замовлення паперу, введіть необхідну кількість рулонів паперу \n'

help_string = ''
info_string = ''
Strings = {
    'start': start_cmd_string,
    'photo_caption': pos_photo_string,
    'help': help_string,
    'info': info_string,

}
# import re
#
# POS_SN_VX520 = r'^\d{9}'
# print(re.findall(POS_SN_VX520, '123456789'))
#
# POS_SN_X_990 = r'{V}'