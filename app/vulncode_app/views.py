#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/vulnerablecode/
# The VulnerableCode software is licensed under the Apache License version 2.0.
# Data generated with VulnerableCode require an acknowledgment.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with VulnerableCode or any VulnerableCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with VulnerableCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  VulnerableCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  VulnerableCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/vulnerablecode/ for support and download.

import json

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from vulncode_app.serializers import ImpactedPackageSerializer
from vulncode_app.models import ImpactedPackage
from vulncode_app.models import Package
from vulncode_app import api_data


class VulnerabilityData(APIView):
    def get(self, request, package_name):
        vulnerability = []
        extract = []
        summary = []
        reference_id = []
        version = []

        pk = Package.objects.filter(name=package_name)

        for i, v in enumerate(pk):
            vulnerability.append(ImpactedPackage.objects.filter(pk=v.id))
            extract += ImpactedPackageSerializer(vulnerability[i], many=True).data
            summary.append(extract[i]['vulnerability']['summary'])
            reference_id.append(extract[i]['vulnerability']['reference'][0]['reference_id'])
            version.append(extract[i]['package']['version'])

        response = {
            'name': package_name,
            'version': set(version),
            'vulnerabilities': {
                'summary': set(summary),
                'reference_id': set(reference_id)
            }
        }

        return Response(response)


def package(request, name):
    """
    Queries the cve-search api with just
    a package name.
    """
    raw_data = api_data.data_cve_circl(name=name)
    fields_names = ['id', 'summary', 'cvss']
    extracted_data = api_data.extract_fields(raw_data, fields_names)

    return HttpResponse(json.dumps(extracted_data))


def package_version(request, name, version):
    """
    Queries the cve-search api with a package
    name and version.
    """
    raw_data = api_data.data_cve_circl(name=name, version=version)
    fields_names = ['id', 'summary', 'cvss']
    extracted_data = api_data.extract_fields(raw_data, fields_names, version=True)

    return HttpResponse(json.dumps(extracted_data))
