# from TextToDF import TextDF
# from datetime import datetime
# from Exceptions import DateError
# from API import *
# now = datetime.now()
# print(now)
#
#
# class interface:
#     def __init__(self,path,enc = False):
#         self.df = TextDF(path,enc)
#         self.__is_enc = enc
#
#     def menu(self):
#         while True:
#             print('-----------------------------------------------------------------')
#             print('\nWhat action would you want to do?\n1.Summarize chat with AI.\n2.Decide who is right in an argument.\n3.Current + top 5 message count/week.')
#             choice = input()
#
#             if choice == '1':
#                 self.sum_chat()
#
#
#             if choice == '2':
#                 chat = self.get_df()
#                 lang = input('\nChoose a language: 1. English. 2. Hebrew.\n')
#                 while True:
#                     if lang != '1' and lang != '2':
#                         continue
#                     elif lang == '1':
#                         print('\nAI response:\n')
#                         answer = self.df.dec_message(Comunnicate(
#                             prompt = f"Analyze the following conversation factually and determine who is correct based on the statements given. Provide only the name of the correct person and a two-sentences short explanation. Do not add opinions. Chat: {chat}",
#                             temperature=0.3, max_tokens=200, content='You are a smart summarize expert'))
#                     else:
#                         print('\nAI response:\n')
#                         answer = self.df.dec_message(Comunnicate(
#                             prompt = f"תנתח את השיחה הבאה באופן עובדתי ותקבע מי צודק בהתבסס על הטענות שנאמרו. ציין רק את שם האדם הצודק ותן הסבר במשפט אחד בלבד. אל תוסיף דעות. שיחה: {chat}",
#                             temperature=0.4, max_tokens=200, content='You are a smart summarize expert'))
#                     print(answer)
#                     break
#
#             if choice == '3':
#                 self.df.count_by_week()
#
#     def sum_chat(self):
#         chat = self.get_df()
#         lang = input('\nChoose a language: 1. English. 2. Hebrew.\n')
#         while True:
#             if lang != '1' and lang != '2':
#                 continue
#             elif lang == '1':
#                 print('\nAI response:\n')
#                 answer = self.df.dec_message(Comunnicate(
#                     prompt=f"Summarize the following chat factually in **no more than 3 sentences**. Do not ask questions. Be concise. Do not add opinions, explanations, or unnecessary details. Chat: {chat}",
#                     temperature=0.4, max_tokens=200, content='You are a smart summarize expert'))
#             else:
#                 print('\nAI response:\n')
#                 answer = self.df.dec_message(Comunnicate(
#                     prompt=f"תענה בעברית בלבד וסכם את השיחה הבאה באופן עובדתי. אל תשאל שאלות. כלול את שמות כל המשתתפים. אל תוסיף דעות, הסברים או עצות. שיחה: {chat}",
#                     temperature=0.4, max_tokens=200, content='You are a smart summarize expert'))
#             print(chat)
#             print(answer)
#             break
#     def get_df(self):
#         while True:
#             try:
#                 start = self.enter_date_time()
#                 chatdf = self.df.start_from(*start)
#                 while True:
#                     end = input('1 for end time or leave blank in order to auto-end (after 4500 characters):\n')
#                     if end == '1':
#                         end = self.enter_date_time(end=True)
#                         chatdf = self.df.end_at(*end, chatdf)
#                         break
#                     elif end == '':
#                         break
#                 return self.df.df_to_text(chatdf)
#             except DateError as e:
#                 print(e)
#     def enter_date_time(self,end = False):
#         valid_date = False
#         while not valid_date:
#             print(f'Please select date no later than {self.df.get_last_date_str()}')
#             if end:
#                 date_input = input("Format- DD MM YYYY, leave blank for current date:\n")
#             else:
#                 date_input = input("Format- DD MM YYYY:\n")
#             try:
#                 date_input = self.check_date(date_input,end)
#                 str_date = '\\'.join([str(i) for i in date_input])
#                 print(f'Date: {str_date}')
#                 valid_date = True
#                 valid_time = False
#                 while not valid_time:
#                     try:
#                         time_input = input("Please enter time\nFormat- HH MM:\n")
#                         time_input = self.check_time(time_input)  # Validate time
#                         str_time = ':'.join([str(i) for i in time_input])
#                         valid_time = True
#                         final_datetime = str_date + ', ' + str_time  # Combine date & time
#                         print(f"Final Date & Time: {final_datetime}")
#
#                         return time_input + date_input
#                     except ValueError as e:
#                         print(e)
#
#             except ValueError as e:
#                 print(e)
#
#
#
#
#
#
#     def check_date(self,date_input, end = False):
#         if date_input == '' and end:
#             now = datetime.now()
#             return (now.day, now.month, now.year)
#         elif not all(i.isdigit() or i == ' ' for i in date_input) or len(date_input.split()) != 3 or len(date_input.split()[-1]) != 4:
#             raise ValueError("Invalid input! Please enter in DD MM YYYY format.\n")
#         date_input = date_input.split()
#         new = [int(i) for i in date_input]
#         try:
#             datetime(*new[::-1])  # If invalid, this raises ValueError
#             return tuple(new)
#         except ValueError:
#             raise ValueError("Invalid input! Please enter in DD MM YYYY format.\n")
#
#     def check_time(self, time_input):
#         if time_input == '' or not all(i.isdigit() or i == ' ' for i in time_input) or len(time_input.split()) != 2:
#             raise ValueError("Invalid input! Please enter time in HH MM format.\n")
#
#         time_input = time_input.split()
#         new = [int(i) for i in time_input]
#
#         try:
#             if not (0 <= new[0] <= 23 and 0 <= new[1] <= 59):
#                 raise ValueError
#             return tuple(new)
#         except ValueError:
#             raise ValueError("Invalid time! Please enter a valid time in HH MM format.\n")
#
# inter = interface('/Users/nadav/Downloads/_chat 18.txt', False)
# j = 0
# print('------------------------------------------------------------------------------------')
# # for i in inter.df.start_from(0, 2, 23,2,2025)['Txt']:
# #     j+=1
# #     print(i)
# # print(str(j))
# # inter = interface('/Users/nadav/Downloads/_chat 15.txt', True)
# # print()
# # inter.df.count_by_week()
# inter.sum_chat()
# # print(inter.enter_date_time())