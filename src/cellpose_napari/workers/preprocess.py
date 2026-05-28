import re
import tifffile
import xarray as xr
import importlib


class PreprocessingUtils:

    @staticmethod
    def strToArgs(s):
        result = {}
        if s is None or s == "":
            return result
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
    def extractMethod(s):
        if s is None or s == "":
            return None
        f_name = s[1:]
        if hasattr(xr.DataArray, f_name):
            return getattr(xr.DataArray, f_name, None)
        return None

    @staticmethod
    def extractFunction(s):
        if s is None or s == "":
            return None
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
    def strToFunction(s):
        if s is None or s == "":
            return None
        elif s.startswith("."):
            print("Using preprocessing method:", s)
            return PreprocessingUtils.extractMethod(s)
        else:
            print("Using preprocessing function:", s)
            return PreprocessingUtils.extractFunction(s)
        
    @staticmethod
    def applyPreprocessing(img, func_str, args_str):
        function = PreprocessingUtils.strToFunction(func_str)
        args = PreprocessingUtils.strToArgs(args_str)
        if function is not None:
            return function(img, **args)
        else:
            return img
    
    @staticmethod
    def getPreprocessingFx(func_str, args_str):
        function = PreprocessingUtils.strToFunction(func_str)
        args     = PreprocessingUtils.strToArgs(args_str)
        if function is not None:
            return lambda img: function(img, **args)
        else:
            return lambda img: img
        

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

    print(xa.sizes['T'])

    # Applying the preprocessing
    xa = PreprocessingUtils.applyPreprocessing(
        xa, 
        preprocessing_function_str, 
        preprocessing_arguments_str
    )
    tifffile.imwrite("/home/clement/Desktop/cellpose_napari_wd/mipped.tif", xa)