def get_correct_substring(player_text: str, text: str):
    index = 0
    while player_text[index] == text[index]:
        index += 1
    return text[0:index]
    

player_text = 'This isa thing'
text = 'This isb thing'

print(get_correct_substring(player_text, text))