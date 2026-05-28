import re
import tifffile
import xarray as xr
import importlib


class PreprocessingUtils:

    @staticmethod
    def str_to_args(s):
        result = {}
        pattern = r"(\w+)=('(?:[^']*)'|\"(?:[^\"]*)\"|None|\(.*?\)|\[.*?\]|[^,]+)"
        for match in re.finditer(pattern, s):
            key, value = match.group(1), match.group(2)
            if value == 'None':
                result[key] = None
            elif value.startswith(("'", '"')):
                result[key] = value[1:-1]
            else:
                result[key] = eval(value.strip())
        return result


    @staticmethod
    def extract_method(obj, s):
        f_name = s[1:]
        if hasattr(obj, f_name):
            return getattr(type(obj), f_name, None)
        return None


    @staticmethod
    def extract_function(s):
        function_parts = s.split(".")
        module_path = ".".join(function_parts[:-1])
        function_name = function_parts[-1]

        try:
            module = importlib.import_module(module_path)
            preprocessing_function = getattr(module, function_name)
        except Exception as e:
            print(f"Error importing preprocessing function: {e}")
            preprocessing_function = None

        return preprocessing_function

    @staticmethod
    def str_to_function(obj, s):
        if s.startswith("."):
            print("Using preprocessing method:", s)
            return PreprocessingUtils.extract_method(obj, s)
        else:
            print("Using preprocessing function:", s)
            return PreprocessingUtils.extract_function(s)
        
    @staticmethod
    def apply_preprocessing(img, func_str, args_str):
        function = PreprocessingUtils.str_to_function(img, func_str)
        args = PreprocessingUtils.str_to_args(args_str)
        if function is not None:
            return function(img, **args)
        else:
            return img
        

if __name__ == "__main__":
    # Args received as strings from the options:
    arg_type = 'method'
    pool = {
        'method': {
            'fx'  : "numpy.max",
            'args': "axis=0"
        },
        'function': {
            'fx'  : ".max",
            'args': "dim='Z'"
        }
    }    
    preprocessing_function_str  = pool[arg_type]['fx']
    preprocessing_arguments_str = pool[arg_type]['args']
    
    # Loading the data
    img_path = "/home/clement/Desktop/cellpose_napari_wd/to-mip.tif"
    img = tifffile.imread(img_path)
    xa = xr.DataArray(img, dims=["T", "Z", "Y", "X"])

    # Applying the preprocessing
    xa = PreprocessingUtils.apply_preprocessing(
        xa, 
        preprocessing_function_str, 
        preprocessing_arguments_str
    )
    tifffile.imwrite("/home/clement/Desktop/cellpose_napari_wd/mipped.tif", xa)