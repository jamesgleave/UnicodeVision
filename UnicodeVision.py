from Converter import Converter
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", help="The mode of the conversion. This can be either s (stream) or u (upload)",
                        required=False, default='s')
    parser.add_argument("--path", help="The absolute path leading to a video or image",
                        required=False)
    parser.add_argument("--scale", help="The scale of the image.",
                        required=False)
    parser.add_argument("--contrast", help="The contrast.",
                        required=False)
    parser.add_argument("--sharpen", help="The sharpen value.",
                        required=False)
    parser.add_argument("--framerate", help="The framerate of the replay",
                        required=False, default=25)
    parser.add_argument("--invert", help="Invert the photo pixel values.",
                        required=False, default=False)
    parser.add_argument("--autoscale", help="Automatically rescales the image to fit your screen",
                        required=False, default=True)
    parser.add_argument("--rotate", help="Rotate the input",
                        required=False)

    args = parser.parse_args()

    converter = Converter(args.framerate)

    default_stream_values = [0.07, 1.0, 1.0, False]
    default_upload_values = [0.15, 1.5, 2.1, False, 0]

    if args.mode == 's':
        # size_ratio = 0.07, contrast = 1.0, sharpen = 1.0, invert = False
        size_ratio = float(default_stream_values[0] if args.scale is None else args.scale)
        contrast = float(default_stream_values[1] if args.contrast is None else args.contrast)
        sharpen = float(default_stream_values[2] if args.sharpen is None else args.sharpen)
        invert = args.invert
        autoscale = args.autoscale

        converter.live_stream(size_ratio, contrast, sharpen, invert, autoscale)
    else:
        assert args.path is not None, "If you are uploading a photo/video you must include the file path"
        size_ratio = float(default_upload_values[0] if args.scale is None else args.scale)
        contrast = float(default_upload_values[1] if args.contrast is None else args.contrast)
        sharpen = float(default_upload_values[2] if args.sharpen is None else args.sharpen)
        rotate = float(default_upload_values[4] if args.rotate is None else args.rotate)
        invert = args.invert
        autoscale = args.autoscale
        import mimetypes

        mimetypes.init()
        mime_start = mimetypes.guess_type(args.path)[0]

        if mime_start is not None:
            mime_start = mime_start.split('/')[0]

            if mime_start == 'video':
                converter.convert_video(args.path, size_ratio, contrast, sharpen, invert, rotate, autoscale)
            elif mime_start == 'image':
                converter.convert_image(args.path, size_ratio, contrast, sharpen, invert, rotate, autoscale)


        converter.show()

