from TextToDFWeb import TextDF, get_participants
from datetime import datetime
from Exceptions import DateError
from API import Comunnicate
import re

def extract_reduced_conversation(text): #Taken form ChatGPT, takes 3 sentences out of 9
    # Split text into sentences using ":" as the primary separator
    sentences = re.split(r'(?<=[:])\s*', text)  # Keeps ":" at the end of each sentence

    # Process in chunks of 9, selecting 3 strategically
    reduced_sentences = []
    for i in range(0, len(sentences), 9):  # Process in blocks of 9
        chunk = sentences[i:i + 9]  # Get 9 sentences (or fewer at the end)

        if len(chunk) >= 3:
            # Pick sentences: first, middle, and last (adjust if fewer than 9)
            reduced_sentences.append(chunk[0])  # First sentence
            reduced_sentences.append(chunk[len(chunk) // 2])  # Middle sentence
            reduced_sentences.append(chunk[-1])  # Last sentence
        else:
            # If less than 3 remaining, just add all
            reduced_sentences.extend(chunk)

    # Join the reduced sentences back
    reduced_text = " ".join(reduced_sentences)
    return reduced_text
now = datetime.now()
print(now)


class interface:
    def __init__(self,ready_str,enc = False):

        self.df = TextDF(ready_str = ready_str, enc = enc)
        self.__is_enc = enc

    def menu(self):
        while True:
            print('-----------------------------------------------------------------')
            print('\nWhat action would you want to do?\n1.Summarize chat with AI.\n2.Decide who is right in an argument.\n3.Current + top 5 message count/week.')
            choice = input()

            if choice == '1':
                self.sum_chat('1')


            if choice == '2':
                chat = self.get_df()
                lang = input('\nChoose a language: 1. English. 2. Hebrew.\n')
                while True:
                    if lang != '1' and lang != '2':
                        continue
                    elif lang == '1':
                        print('\nAI response:\n')
                        answer = self.df.dec_message(Comunnicate(
                            prompt = f"Analyze the following conversation factually and determine who is correct based on the statements given. Provide only the name of the correct person and a two-sentences short explanation. Do not add opinions. Chat: {chat}",
                            temperature=0.3, max_tokens=200, content='You are a smart summarize expert'))
                    else:
                        print('\nAI response:\n')
                        answer = self.df.dec_message(Comunnicate(
                            prompt = f"סכם את השיחה בעברית בלבד. שני משפטים בלבד – אין להוסיף יותר. השתמש בכל שמות המשתתפים. אין להוסיף דעות, הסברים או פרטים נוספים. שיחה: {chat}",
                            temperature=0.4, max_tokens=200, content='You are a smart summarize expert'))
                    print(answer)
                    break

            if choice == '3':
                self.df.count_by_week()

    def sum_chat(self, lang, start_time, end_time):
        chat = self.get_df(start_time,end_time)
        if chat is not None:
            txt = chat[1]
            if lang == '1':
                print('\nAI response:\n')
                answer = self.df.dec_message(Comunnicate(
                    prompt=f"Summarize the following chat factually in **no more than 2 sentences**. Do not ask questions. Be concise. Do not add opinions, explanations, or unnecessary details. Chat: {txt}",
                    temperature=0.4, max_tokens=200, content='You are a smart summarize expert'))
            else:
                print('\nAI response:\n')
                answer = self.df.dec_message(Comunnicate(
                    prompt = f"השב בעברית בלבד. השב רק בשני משפטים. אל תוסיף הסברים או דעות. הזכר את כל שמות המשתתפים. שיחה: {chat[1]}",
                    temperature=0.4, max_tokens=200, content='You are a smart summarize expert'))
            print(get_participants(chat[0]))
            print('chat:' + txt)
            print(answer)

            return 'Participants: '+get_participants(chat[0]) + '<br><br>' + answer.replace('.', '.<br>')
        return ''

    def arg_chat(self, lang, start_time,end_time):
        chat = self.get_df(start_time,end_time)[1]
        if lang == '1':
            print('\nAI response:\n')
            answer = self.df.dec_message(Comunnicate(
                prompt=f"Analyze the following conversation factually and determine who is correct based on the statements given. Provide only the name of the correct person and a two-sentences short explanation. Do not add opinions. Chat: {chat}",
                temperature=0.3, max_tokens=200, content='You are a smart summarize expert')) + '.'
        else:
            print('\nAI response:\n')
            answer = self.df.dec_message(Comunnicate(
                prompt=f"תנתח את השיחה הבאה באופן עובדתי ותקבע מי צודק בהתבסס על הטענות שנאמרו. ציין רק את שם האדם הצודק ותן הסבר במשפט אחד בלבד. אל תוסיף דעות. שיחה: {chat}",
                temperature=0.4, max_tokens=200, content='You are a smart summarize expert')) + '.'
        return answer

    def get_df(self,start_time ,end_time):
        try:
            chatdf = self.df.start_from(start_time)
            if end_time is not None:
                chatdf = self.df.end_at(end_time, chatdf)
            return chatdf, self.df.df_to_text(chatdf).replace('\r','').encode("utf-8").decode("utf-8")  # Normalize encoding
        except DateError as e:
            return None
    def is_funny(self, name):
        df = self.df.specific_author(name)
        chat = self.df.df_to_text(df).replace('\r','')
        chat = extract_reduced_conversation(chat)
        print(len(chat))
        answer1 = self.df.dec_message(Comunnicate(
            prompt=f"**Begginer English level** Analyze the personality and communication style of the author based on the messages provided. Describe their vibe **in one sentence**, making it unique to their tone, word choice, and message patterns. Avoid generic statements. Messages: {chat}",
            temperature=0.4, max_tokens=100,
            content="You specialize in analyzing personalities and providing precise, distinct, and insightful summaries. giving simple understandable words"))
        answer2 = self.df.dec_message(Comunnicate(
            prompt=f"**Easy English** Summarize the general tone and subjects of the chats sent. **two sentences**. Messages: {chat}",
            temperature=0.5, max_tokens=100,
            content="You specialize in analyzing chats and providing precise, distinct, and insightful summaries. giving simple understandable words"))

        print(answer1)
        print(answer2)
        return answer1,answer2

    def enter_date_time(self,end = False):
        valid_date = False
        while not valid_date:
            print(f'Please select date no later than {self.df.get_last_date_str()}')
            if end:
                date_input = input("Format- DD MM YYYY, leave blank for current date:\n")
            else:
                date_input = input("Format- DD MM YYYY:\n")
            try:
                date_input = self.check_date(date_input,end)
                str_date = '\\'.join([str(i) for i in date_input])
                print(f'Date: {str_date}')
                valid_date = True
                valid_time = False
                while not valid_time:
                    try:
                        time_input = input("Please enter time\nFormat- HH MM:\n")
                        time_input = self.check_time(time_input)  # Validate time
                        str_time = ':'.join([str(i) for i in time_input])
                        valid_time = True
                        final_datetime = str_date + ', ' + str_time  # Combine date & time
                        print(f"Final Date & Time: {final_datetime}")

                        return time_input + date_input
                    except ValueError as e:
                        print(e)

            except ValueError as e:
                print(e)






    def check_date(self,date_input, end = False):
        if date_input == '' and end:
            now = datetime.now()
            return (now.day, now.month, now.year)
        elif not all(i.isdigit() or i == ' ' for i in date_input) or len(date_input.split()) != 3 or len(date_input.split()[-1]) != 4:
            raise ValueError("Invalid input! Please enter in DD MM YYYY format.\n")
        date_input = date_input.split()
        new = [int(i) for i in date_input]
        try:
            datetime(*new[::-1])  # If invalid, this raises ValueError
            return tuple(new)
        except ValueError:
            raise ValueError("Invalid input! Please enter in DD MM YYYY format.\n")

    def check_time(self, time_input):
        if time_input == '' or not all(i.isdigit() or i == ' ' for i in time_input) or len(time_input.split()) != 2:
            raise ValueError("Invalid input! Please enter time in HH MM format.\n")

        time_input = time_input.split()
        new = [int(i) for i in time_input]

        try:
            if not (0 <= new[0] <= 23 and 0 <= new[1] <= 59):
                raise ValueError
            return tuple(new)
        except ValueError:
            raise ValueError("Invalid time! Please enter a valid time in HH MM format.\n")

# inter = interface('/Users/nadav/Downloads/_chat 4 copy.txt', False)
# j = 0
# print('------------------------------------------------------------------------------------')
# for i in inter.df.start_from(0, 2, 23,2,2025)['Txt']:
#     j+=1
#     print(i)
# print(str(j))
# inter = interface('/Users/nadav/Downloads/_chat 15.txt', True)
# print()
# inter.df.count_by_week()
# inter.sum_chat()
# print(inter.enter_date_time())