from dataclasses import dataclass

@dataclass
class AddDepartmentReqDTO:
    name:            str
    companyId:       int
    description:     str = None