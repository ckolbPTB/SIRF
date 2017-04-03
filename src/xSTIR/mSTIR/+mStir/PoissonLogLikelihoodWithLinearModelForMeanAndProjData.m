classdef PoissonLogLikelihoodWithLinearModelForMeanAndProjData < ...
        mStir.PoissonLogLikelihoodWithLinearModelForMean
% Class for STIR PoissonLogLikelihoodWithLinearModelForMeanAndProjData object,
% see
% http://stir.sourceforge.net/documentation/doxy/html/classstir_1_1PoissonLogLikelihoodWithLinearModelForMeanAndProjData.html

% CCP PETMR Synergistic Image Reconstruction Framework (SIRF).
% Copyright 2015 - 2017 Rutherford Appleton Laboratory STFC.
% Copyright 2015 - 2017 University College London.
% 
% This is software developed for the Collaborative Computational
% Project in Positron Emission Tomography and Magnetic Resonance imaging
% (http://www.ccppetmr.ac.uk/).
% 
% Licensed under the Apache License, Version 2.0 (the "License");
% you may not use this file except in compliance with the License.
% You may obtain a copy of the License at
% http://www.apache.org/licenses/LICENSE-2.0
% Unless required by applicable law or agreed to in writing, software
% distributed under the License is distributed on an "AS IS" BASIS,
% WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
% See the License for the specific language governing permissions and
% limitations under the License.

    methods
        function self = ...
                PoissonLogLikelihoodWithLinearModelForMeanAndProjData(obj_fun)
            self.name =...
                'PoissonLogLikelihoodWithLinearModelForMeanAndProjData';
            if nargin < 1
                self.handle = calllib('mstir', 'mSTIR_newObject', self.name);
            else
                self.handle = calllib...
                    ('mutilities', 'mCopyOfObjectHandle', obj_fun.handle);
            end
        end
        function delete(self)
            calllib('mutilities', 'mDeleteDataHandle', self.handle)
            self.handle = [];
        end
        function set_input_filename(self, filename)
            mStir.setParameter(self.handle, self.name,...
                'input_filename', filename, 'c')
        end
        function set_zero_seg0_end_planes(self, flag)
            if flag
                str = 'true';
            else
                str = 'false';
            end
            mStir.setParameter(self.handle, self.name,...
                'zero_seg0_end_planes', str, 'c') 
        end
        function set_max_segment_num_to_process(self, n)
            mStir.setParameter(self.handle, self.name, ...
                'max_segment_num_to_process', n, 'i') 
        end
        function set_acquisition_model(self, am)
%         Sets the acquisition model to be used by this objective function.
            mStir.setParameter(self.handle, self.name,...
                'acquisition_model', am, 'h')
        end
        function am = get_acquisition_model(self)
%         Returns the acquisition model used by this objective function.
            am = mStir.AcquisitionModelUsingMatrix();
            am.handle = calllib('mstir', 'mSTIR_parameter',...
                self.handle, self.name, 'acquisition_model');
            mUtil.checkExecutionStatus...
                ([self.name ':get_acquisition_model'], am.handle)
        end
        function set_acquisition_data(self, am)
%         Sets the acquisition data to be used by this objective function.
            mStir.setParameter(self.handle, self.name,...
                'proj_data_sptr', am, 'h')
        end
    end
end