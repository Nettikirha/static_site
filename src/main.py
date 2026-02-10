from textnode import TextNode, TextType


def main():
    # Create a sample TextNode (using the example from the assignment)
    node = TextNode(
        "This is some anchor text", 
        TextType.LINK, 
        "https://www.boot.dev"
    )
    
    print(node)



if __name__ == "__main__":
    main()