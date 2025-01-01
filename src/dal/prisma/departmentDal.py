from dataclasses import asdict
from src.dto.departmentDtos import AddDepartmentReqDTO
from src.prisma import prisma


async def getDepartmentById(departmentId):
    
    return await prisma.department.find_first(
        where={"id": departmentId},
        select={
            "id": True,  # Select the 'id' field
            "name": True  # Select the 'name' field
        }
    )


async def addDepartment(addDepartmentDTO: AddDepartmentReqDTO):
    # department_data = asdict(addDepartmentDTO)

    # Debug: Print out the values being passed to Prisma
    # print("Department Data:", department_data)
    # return await prisma.department.create({"data": department_data})
    return await prisma.department.create({
        "name": addDepartmentDTO.name,
        "companyId": addDepartmentDTO.companyId,
        "description": addDepartmentDTO.description
    })
