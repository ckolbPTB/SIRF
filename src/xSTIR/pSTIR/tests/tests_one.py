'''pSTIR tests

CCP PETMR Synergistic Image Reconstruction Framework (SIRF)
Copyright 2015 - 2017 Rutherford Appleton Laboratory STFC
2017 Casper da Costa-Luis

This is software developed for the Collaborative Computational
Project in Positron Emission Tomography and Magnetic Resonance imaging
(http://www.ccppetmr.ac.uk/).

Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
'''
import math
from pSTIR import *


def norm(v):
    vv = v*v
    nv = v.size
    # return vv.sum()/nv
    return math.sqrt(vv.sum()/nv)


def var(v):
    """function to compute the variance after conversion to double to avoid
    rounding problems with older numpy versions
    """
    return v.astype(numpy.float64).var()


def test_main():
    # create matrix to be used by the acquisition model
    matrix = RayTracingMatrix()
    matrix.set_num_tangential_LORs(2)

    # create acquisition model
    am = AcquisitionModelUsingMatrix()
    am.set_matrix(matrix)

    # locate the input data file folder
    data_path = petmr_data_path('pet')

    # PET acquisition data to be read from this file
    raw_data_file = existing_filepath(data_path, 'Utahscat600k_ca_seg4.hs')
    ad = AcquisitionData(raw_data_file)
    adata = ad.as_array()
    s = norm(adata)
    v = var(adata)
    check_tolerance(2.510818, s)
    check_tolerance(5.444323, v)
    #print('acquisitions mean sum of squares: %f, variance: %f' % (s, v))

    # create filter
    filter = TruncateToCylinderProcessor()

    # create initial image estimate
    image_size = (111, 111, 31)
    voxel_size = (3, 3, 3.375) # voxel sizes are in mm
    image = ImageData()
    image.initialise(image_size, voxel_size)
    image.fill(1.0)
    
    filter.apply(image)
    image_arr = image.as_array()
    s = norm(image_arr)
    v = var(image_arr)
    check_tolerance(0.876471, s)
    check_tolerance(0.178068, v)
    #print('image mean sum of squares: %f, variance: %f' % (s, v))

    # create prior
    prior = QuadraticPrior()
    prior.set_penalisation_factor(0.5)

    # set number of subsets
    num_subsets = 12

    # create objective function
    obj_fun = make_Poisson_loglikelihood(ad)
    obj_fun.set_acquisition_model(am)
    obj_fun.set_num_subsets(num_subsets)
    obj_fun.set_up(image)

    # select subset
    subset = 0

    # get sensitivity as ImageData
    ss_img = obj_fun.get_subset_sensitivity(subset)

    # get back projection of the ratio of measured to estimated acquisition data
    grad_img = obj_fun.get_backprojection_of_acquisition_ratio(image, subset)

    # get gradient of prior as ImageData
    pgrad_img = prior.get_gradient(image)

    # copy to Python arrays
    image_arr = image.as_array()
    ss_arr = ss_img.as_array()
    grad_arr = grad_img.as_array()
    pgrad_arr = pgrad_img.as_array()

    # update image data
    ss_arr[ss_arr < 1e-6] = 1e-6 # avoid division by zero
    update = grad_arr/(ss_arr + pgrad_arr/num_subsets)
    image_arr = image_arr*update

    s = norm(image_arr)
    v = var(image_arr)
    check_tolerance(0.012314, s)
    check_tolerance(0.000052, v, 1e-4)
    #print('image mean sum of squares: %f, variance: %f' % (s, v))
    s = norm(update)
    v = var(update)
    check_tolerance(3.846513, s)
    check_tolerance(14.775219, v)
    #print('update mean sum of squares: %f, variance: %f' % (s, v))
    s = norm(ss_arr)
    v = var(ss_arr)
    check_tolerance(27.990159, s)
    check_tolerance(207.401144, v)
    #print('sensitivity mean sum of squares: %f, variance: %f' % (s, v))
    s = norm(grad_arr)
    v = var(grad_arr)
    check_tolerance(98.049032, s)
    check_tolerance(9599.796540, v)
    #print('gradient mean sum of squares: %f, variance: %f' % (s, v))
    s = norm(pgrad_arr)
    v = var(pgrad_arr)
    check_tolerance(0.710633, s)
    check_tolerance(0.505000, v)
    #print('prior gradient mean sum of squares: %f, variance: %f' % (s, v))