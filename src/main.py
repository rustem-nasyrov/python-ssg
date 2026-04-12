from textnode import TextNode, TextType

def main():
    text = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(text)

main()