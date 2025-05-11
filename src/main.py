from textnode import TextNode, TextType

def main():
    obj = TextNode("Hello", TextType.NORMAL_TEXT, "https://example.com")
    stringa = obj.__repr__()
    print(stringa)

main()