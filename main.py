from processor.image_processor import (
    load_image, save_image, edge_detection, pencil_sketch, thresholding, posterization, contour_highlight
)
import cv2


def main():
    print("Loading image...")
    try:
        image = load_image()
    except FileNotFoundError as e:
        print(e)
        return

    print("Choose a processing method:")
    print("1: Edge Detection")
    print("2: Pencil Sketch")
    print("3: Thresholding")
    print("4: Posterization")
    print("5: Contour Highlighting")

    choice = input("Enter the number of your choice: ")
    processed_image = None

    if choice == "1":
        processed_image = edge_detection(image)
    elif choice == "2":
        processed_image = pencil_sketch(image)
    elif choice == "3":
        processed_image = thresholding(image)
    elif choice == "4":
        levels = int(input("Enter the number of posterization levels (e.g., 4): "))
        processed_image = posterization(image, levels)
    elif choice == "5":
        processed_image = contour_highlight(image)
    else:
        print("Invalid choice.")
        return

    # Display and save the processed image
    cv2.imshow("Processed Image", processed_image)
    save_image(processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
