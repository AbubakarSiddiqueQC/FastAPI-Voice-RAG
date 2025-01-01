from fastapi import APIRouter

import src.dal.prisma.departmentDal  as departmentDal
from src.dto.departmentDtos import AddDepartmentReqDTO


router = APIRouter(
    prefix="/department",  
    tags=["department"]   
)

@router.get("/getDeparment", description="descrip")
async def getDeparment(departmentId):
    return await departmentDal.getDepartmentById(departmentId)



@router.post("/addDeparment")
async def addDeparment(addDepartmentDTO: AddDepartmentReqDTO):
    addDepartmentDTO.createdby = 1
    return await departmentDal.addDepartment(addDepartmentDTO)




