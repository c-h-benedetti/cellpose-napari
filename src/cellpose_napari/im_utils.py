import xarray as xr

class ImageUtils(object):

    @staticmethod
    def ensureAxes(da: xr.DataArray, axes: list[str] = ["T", "Z", "C", "Y", "X"]) -> xr.DataArray:
        if da is None:
            return None
        for i, ax in enumerate(axes):
            if ax not in da.dims:
                da = da.expand_dims({ax: 1}, axis=i)
        return da
    
    @staticmethod
    def removeExtraAxes(da: xr.DataArray, axes: list[str] = ["T", "Z", "C", "Y", "X"]) -> xr.DataArray:
        if da is None:
            return None
        for ax in da.dims:
            if ax not in axes:
                da = da.squeeze(dim=ax)
        return da
    
    @staticmethod
    def removeAxis(da: xr.DataArray, axis: str) -> tuple[xr.DataArray, int]:
        if da is None:
            return None, -1
        rank = -1
        if axis in da.dims:
            rank = da.dims.index(axis)
            da = da.squeeze(dim=axis)
        return da, rank
    
    @staticmethod
    def emplaceAxis(da: xr.DataArray, axis: str, position: int) -> xr.DataArray:
        if da is None:
            return None
        if axis not in da.dims:
            da = da.expand_dims({axis: 1}, axis=position)
        return da
    
    @staticmethod
    def asFilterSize(img: xr.DataArray, calib: dict[str, float], size: float) -> tuple[int, ...]:
        size_x = size
        size_y = size
        size_z = size * calib['Z'] / calib['X']
        base = [1 for _ in img.dims]
        base[img.dims.index('X')] = int(round(size_x / calib['X']))
        base[img.dims.index('Y')] = int(round(size_y / calib['Y']))
        base[img.dims.index('Z')] = int(round(size_z / calib['Z']))
        return tuple(base)