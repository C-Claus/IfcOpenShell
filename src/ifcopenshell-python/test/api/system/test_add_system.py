# IfcOpenShell - IFC toolkit and geometry engine
# Copyright (C) 2022 Dion Moult <dion@thinkmoult.com>
#
# This file is part of IfcOpenShell.
#
# IfcOpenShell is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IfcOpenShell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IfcOpenShell.  If not, see <http://www.gnu.org/licenses/>.

import test.bootstrap
import ifcopenshell.api


class TestAddSystem(test.bootstrap.IFC4):
    def test_adding_a_system(self):
        system = ifcopenshell.api.run("system.add_system", self.file, ifc_class="IfcSystem")
        system2 = ifcopenshell.api.run("system.add_system", self.file, ifc_class="IfcDistributionSystem")
        assert system.is_a("IfcSystem")
        assert system2.is_a("IfcDistributionSystem")
