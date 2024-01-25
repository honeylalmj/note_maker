# Note Maker App



## Overview

The Note Maker App is a simple application built with KivyMD, Python, and JSON that allows users to create, save, view, and delete notes based on specific dates.

## Features

- **Create Note**: Users can create a note by providing a date and entering the note content. The note is saved when the save button is clicked.

- **View Notes**: The app provides an option to view saved notes. Users can see all the notes under a particular date.

- **Delete Note**: Users can delete a note by clicking the delete button next to the date button in the view option.

## Technologies Used

- **KivyMD**: The user interface is built using KivyMD, a Material Design component library for Kivy.

- **Python**: The backend logic is implemented in Python.

- **JSON**: Notes are saved and managed using JSON for data persistence.

## Installation

### Option 1: Using Source Code

1. Clone the repository:

   ```bash
   git clone https://github.com/honeylalmj/note_maker.git
   cd note-maker-app


2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python main.py
   ```

### Option 2: Using Executable (macOS)

Git repository includes an executable file for macOS. Follow the steps below:

1. Download the executable file named **macosexe**.

2. Download the JSON file also.

3. Place both the executable file and the JSON file in the same folder.

4. Double-click the executable file to directly run the app. This method doesn't require any programming software.

**Note:** Ensure that the JSON file is present in the same directory as the executable file for proper data loading.

## Usage

1. Launch the app.

2. Click on the "Create Note" option to add a new note by providing a date and entering the note content.

3. Click on the "View Notes" option to see all the saved notes. Select a date to view notes saved under that date.

4. To delete a note, go to the "View Notes" option, choose the date, and click the delete button.

## Contributing

If you would like to contribute to the project, please follow the steps below:

1. Fork the repository.

2. Create a new branch for your feature:

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m 'Add new feature'
   ```

4. Push to the branch:

   ```bash
   git push origin feature-name
   ```

5. Create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```
