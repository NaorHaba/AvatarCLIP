

class Messages:
    # Website
    ## Page Titles
    HOME_PAGE_TITLE = "# AVR Project - AvatarCLIP"
    HOME_PAGE_SUBTITLE = '## An interactive tool for generating 3D avatars using AvatarCLIP'
    HOME_PAGE_DESCRIPTION = "This project is a web application that allows users to generate 3D avatars using AvatarCLIP."

    VIEW_GENERATED_COARSE_SHAPES_PAGE_TITLE = "Generated Coarse Shapes"
    VIEW_GENERATED_AVATARS_PAGE_TITLE = "Generated Avatars"
    GENERATE_NEW_COARSE_SHAPE_PAGE_TITLE = "Generate New Coarse Shape"
    RENDER_COARSE_SHAPE_PAGE_TITLE = "Render Coarse Shape"
    INITIALIZE_IMPLICIT_AVATAR_PAGE_TITLE = "Initialize Implicit Avatar"
    GENERATE_TEXTURES_PAGE_TITLE = "Generate Textures"
    CONVERT_TO_FBX_PAGE_TITLE = "Convert to FBX"

    ## Page Messages
    SELECTED_VIEW_ITEM_TITLE = "#### {}"

    IF_EXISTS_INSTRUCTION = "Please select what to do if the shape already exists:"

    OVERWRITE_SELECTION = "Overwrite existing results"
    OVERWRITE_NOTICE = "NOTICE! Overwriting '{}'"
    CONTINUE_SELECTION = "Continue training from last checkpoint"
    CONTINUE_NOTICE = "Continuing training for '{}'"

    ### View Generated Coarse Shapes
    VIEW_GENERATED_COARSE_SHAPES_SELECT_SHAPE = "Select a shape to view"
    VIEW_GENERATED_COARSE_SHAPES_OBJ_FILE_STATUS_TITLE = "OBJ file"
    VIEW_GENERATED_COARSE_SHAPES_RENDER_FOLDER_STATUS_TITLE = "Render folder"
    VIEW_GENERATED_COARSE_SHAPES_IMPLICIT_FOLDER_STATUS_TITLE = "Implicit folder"  # TODO find a better name for implicit

    ### View Generated Avatars
    VIEW_GENERATED_AVATARS_SELECT_AVATAR = "Select an avatar to view"
    VIEW_GENERATED_AVATARS_TEXTURE_FOLDER_STATUS_TITLE = "Texture folder"
    VIEW_GENERATED_AVATARS_FBX_FILE_STATUS_TITLE = "FBX file"

    ### Generate New Coarse Shape
    GENERATE_NEW_COARSE_SHAPE_DESCRIPTION = "Enter a coarse shape description (e.g a tall person, a skinny person etc.):"
    GENERATE_NEW_COARSE_SHAPE_FORM_SUBMIT_BUTTON = "Generate Coarse Shape"
    GENERATE_NEW_COARSE_SHAPE_RETRY_MESSAGE = "Please choose a different description or check the overwrite checkbox"

    ### Render Coarse Shape
    RENDER_COARSE_SHAPE_SELECT_SHAPE = "Select a shape to render"
    RENDER_COARSE_SHAPE_FORM_SUBMIT_BUTTON = "Render Coarse Shape"

    ## Initialize Implicit Avatar
    INITIALIZE_IMPLICIT_AVATAR_SELECT_SHAPE = "Select a shape to initialize"
    INITIALIZE_IMPLICIT_AVATAR_FORM_SUBMIT_BUTTON = "Initialize Implicit Avatar"
    CHOOSE_CONFIG = "Choose a config file to use for initialization"
    LARGE_CONFIG = "Large config"
    SMALL_CONFIG = "Small config"

    ## Generate Textures
    GENERATE_TEXTURES_SELECT_SHAPE = "Select a shape to generate textures for"
    GENERATE_TEXTURES_FORM_SUBMIT_BUTTON = "Generate Textures"
    GENERATE_TEXTURES_DESCRIPTION = "Enter the texture description (e.g Batman, Obama etc.):"

    ## Convert to FBX
    CONVERT_TO_FBX_SELECT_AVATAR = "Select an avatar to convert to FBX"
    CONVERT_TO_FBX_FORM_SUBMIT_BUTTON = "Convert to FBX"

    # Error Messages
    FOLDER_DOES_NOT_EXIST = "Folder {} does not exist."
    NO_SHAPE_FOUND_IN_FOLDER = "No shapes found in {}."
    ALREADY_EXISTS = "'{}' already exists."


    # Logic Messages
    CUDA_DEFAULT_TENSOR_TYPE_INFO = "CUDA is available. Setting default tensor type to 'torch.cuda.FloatTensor'"
    NEW_CONFIG_FILE_INFO = "Creating new config file with running parameters: {}"
    LAST_CHECKPOINT_INFO = "Using last checkpoint: {} for training"

    ## generate_coarse_shape
    GENERATE_NEW_COARSE_SHAPE_INFO = "Start generating coarse body shape given the target text: {}"
    GENERATE_NEW_COARSE_SHAPE_SUCCESS = "Coarse body shape generated and saved to {}"

    ## render_coarse_shape
    RENDER_COARSE_SHAPE_INFO = "Start rendering coarse body shape given the target OBJ file: {}"
    RENDER_COARSE_SHAPE_SUCCESS = "Coarse body shape rendered and saved to {}"

    ## initialize_implicit_avatar
    INITIALIZE_IMPLICIT_AVATAR_INFO = "Start initializing implicit avatar for the given coarse shape: {}"
    INITIALIZE_IMPLICIT_AVATAR_SUCCESS = "Implicit avatar initialized and saved according to the config file"

    ## generate_textures
    GENERATE_TEXTURES_INFO = "Start generating textures for the given coarse shape: {}"
    GENERATE_TEXTURES_SUCCESS = "Textures generated and saved according to the config file"