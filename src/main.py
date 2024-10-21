from src.emoji_text import get_emoji_text



def convert_instructions_to_path(instructions):
    path = ""
    for instruction in instructions:
        command = instruction[0]
        if command == 'moveTo':
            path += f"M{instruction[1][0]} {instruction[1][1]} "
        elif command == 'lineTo':
            path += f"L{instruction[1][0]} {instruction[1][1]} "
        elif command == 'qCurveTo':
            path += f"Q{instruction[1][0]} {instruction[1][1]} {instruction[2][0]} {instruction[2][1]} "
        elif command == 'closePath':
            path += "Z "
    return path.strip()


def main():
    font_path = "fonts/GeistMonoVF.woff"  
    text = "TEST"
    emoji = "🥺"

    text_emojis = get_emoji_text(text=text, emoji=emoji, font_path=font_path)
    output = "\n\n".join(text_emojis)
    print(output)



if __name__ == "__main__":
    main()
