

class Messages:
    # Page Titles
    HOME_PAGE_TITLE = "# AVR Project - AvatarCLIP"
    HOME_PAGE_SUBTITLE = '## An interactive tool for generating 3D avatars using AvatarCLIP'
    HOME_PAGE_DESCRIPTION = "This project is a web application that allows users to generate 3D avatars using AvatarCLIP."

    VIEW_GENERATED_COARSE_SHAPES_PAGE_TITLE = "Generated Coarse Shapes"
    VIEW_GENERATED_AVATARS_PAGE_TITLE = "Generated Avatars"
    GENERATE_NEW_COARSE_SHAPE_PAGE_TITLE = "Generate New Coarse Shape"
    RENDER_COARSE_SHAPE_PAGE_TITLE = "Render Coarse Shape"

    # Page Messages
    SELECTED_VIEW_ITEM_TITLE = "#### {}"

    IF_EXISTS_INSTRUCTION = "Please select what to do if the shape already exists:"

    OVERWRITE_SELECTION = "Overwrite existing results"
    OVERWRITE_NOTICE = "NOTICE! Overwriting '{}'"
    CONTINUE_SELECTION = "Continue training from last checkpoint"
    CONTINUE_NOTICE = "Continuing training for '{}'"

    ## View Generated Coarse Shapes
    VIEW_GENERATED_COARSE_SHAPES_SELECT_SHAPE = "Select a shape to view"
    VIEW_GENERATED_COARSE_SHAPES_OBJ_FILE_STATUS_TITLE = "OBJ file"
    VIEW_GENERATED_COARSE_SHAPES_RENDER_FOLDER_STATUS_TITLE = "Render folder"
    VIEW_GENERATED_COARSE_SHAPES_IMPLICIT_FOLDER_STATUS_TITLE = "Implicit folder"  # TODO find a better name for implicit

    ## View Generated Avatars
    VIEW_GENERATED_AVATARS_SELECT_AVATAR = "Select an avatar to view"
    VIEW_GENERATED_AVATARS_TEXTURE_FOLDER_STATUS_TITLE = "Texture folder"
    VIEW_GENERATED_AVATARS_FBX_FILE_STATUS_TITLE = "FBX file"

    ## Generate New Coarse Shape
    GENERATE_NEW_COARSE_SHAPE_DESCRIPTION = "Enter a coarse shape description (e.g a tall person, a skinny person etc.):"
    GENERATE_NEW_COARSE_SHAPE_FORM_SUBMIT_BUTTON = "Generate Coarse Shape"
    GENERATE_NEW_COARSE_SHAPE_RETRY_MESSAGE = "Please choose a different description or check the overwrite checkbox"

    ## Render Coarse Shape
    RENDER_COARSE_SHAPE_SELECT_SHAPE = "Select a shape to render"
    RENDER_COARSE_SHAPE_FORM_SUBMIT_BUTTON = "Render Coarse Shape"

    # Error Messages
    FOLDER_DOES_NOT_EXIST = "Folder {} does not exist."
    NO_SHAPE_FOUND_IN_FOLDER = "No shapes found in {}."
    ALREADY_EXISTS = "'{}' already exists."