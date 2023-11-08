from detection_helpers import *
from tracking_helpers import *
from bridge_wrapper import *
from PIL import Image


def run(
    global_file_path_undetected,
    global_file_name,
    close_loading,
    start_timer,
    stop_timer,
    update_text,
    update_image,
    selected_number
):
    selected_value_str = selected_number.get()
    selected_value_int = int(selected_value_str)
    detector = Detector(
        classes=None
    )  # it'll detect ONLY [person,horses,sports ball]. class = None means detect all classes. List info at: "data/coco.yaml"
    detector.load_model(
        "./weights/best_exp4.pt",
    )  # pass the path to the trained weight file

    # Initialise  class that binds detector and tracker in one class
    tracker = YOLOv7_DeepSORT(
        reID_model_path="./deep_sort/model_weights/mars-small128.pb", detector=detector
    )

    start_timer()
    # output = None will not save the output video
    tracker.track_video(
        update_text,
        update_image,
        global_file_path_undetected,
        output=f"./video_output/{global_file_name}",
        show_live=False,
        skip_frames=selected_value_int,
        count_objects=True,
        verbose=1,
    )
    stop_timer()
    close_loading(f"./video_output/{global_file_name}")
