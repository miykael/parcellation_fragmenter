import numpy as np


def region_indices(lab_obj, regions=None):
	"""
	Add labels to indices of region

    Parameters:
    - - - - -
    lab_obj : GiftiImage
        loaded label object
    """
    cdata = lab_obj.darrays[0].data
    lt = lab_obj.get_labeltable().get_labels_as_dict()
    reg2lab = dict(zip(map(str, lt.values()), lt.keys()))

    if not regions:
        indices = np.arange(len(cdata))
    else:
        indices = []

    	for r in regions:
    		indices.append(np.where(cdata == reg2lab[r])[0])

    	indices = np.concatenate(indices)

	return indices
