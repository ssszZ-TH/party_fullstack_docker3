import React, { lazy, Suspense } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { ThemeProvider } from "./contexts/ThemeContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Loading from "./components/Loading";

// Lazy load pages เพื่อเพิ่มประสิทธิภาพโดยโหลดเฉพาะหน้าเมื่อจำเป็น
const Home = lazy(() => import("./pages/Home"));
const Login = lazy(() => import("./pages/Login"));
const Register = lazy(() => import("./pages/Register"));
const PersonDetail = lazy(() => import("./pages/layer_info/PersonDetail"));
const PassportByCitizenshipId = lazy(
  () => import("./pages/layer_info/PassportByCitizenshipId")
);

// กำหนด array ของ routes สำหรับหน้าเพิ่มเติม
// แต่ละ route มี path และ component ที่ lazy load
// เรียงลำดับตามความยาวของ path จากสั้นไปยาวเพื่อความสวยงามและอ่านง่าย
const routes = [
  { path: "/vite", component: lazy(() => import("./App")) },
  { path: "/users", component: lazy(() => import("./pages/Users")) },
  {
    path: "/v1/person",
    component: lazy(() => import("./pages/layer_info/Person")),
  },
  {
    path: "/v1/country",
    component: lazy(() => import("./pages/layer_type/Country")),
  },
  {
    path: "/v1/passport",
    component: lazy(() => import("./pages/layer_info/Passport")),
  },
  {
    path: "/v1/passport/:paramId",
    component: lazy(() => import("./pages/layer_info/PassportDetail")),
  },
  { path: "/v1/profile", component: lazy(() => import("./pages/Profile")) },
  {
    path: "/v1/partytype",
    component: lazy(() => import("./pages/layer_type/PartyType")),
  },
  {
    path: "/v1/ethnicity",
    component: lazy(() => import("./pages/layer_type/Ethnicity")),
  },
  {
    path: "/v1/personname",
    component: lazy(() => import("./pages/layer_info/PersonName")),
  },
  {
    path: "/v1/incomerange",
    component: lazy(() => import("./pages/layer_type/IncomeRange")),
  },
  {
    path: "/v1/citizenship",
    component: lazy(() => import("./pages/layer_info/Citizenship")),
  },
  {
    path: "/v1/industrytype",
    component: lazy(() => import("./pages/layer_type/IndustryType")),
  },
  {
    path: "/v1/industrybyorganizationid/:paramId",
    component: lazy(
      () => import("./pages/layer_info/IndustryByOrganizationId")
    ),
  },
  {
    path: "/v1/sizebyorganizationid/:paramId",
    component: lazy(() => import("./pages/layer_info/SizeByOrganization")),
  },
  {
    path: "/v1/minoritybyorganizationid/:paramId",
    component: lazy(
      () => import("./pages/layer_info/MinorityByOrganizationId")
    ),
  },
  {
    path: "/v1/minoritytype",
    component: lazy(() => import("./pages/layer_type/MinorityType")),
  },
  {
    path: "/v1/maritalstatus",
    component: lazy(() => import("./pages/layer_info/MaritalStatus")),
  },
  {
    path: "/v1/classifybyeeoc",
    component: lazy(() => import("./pages/layer_info/ClassifyByeeoc")),
  },

  {
    path: "/v1/classifybysize",
    component: lazy(() => import("./pages/layer_info/ClassifyBySize")),
  },
  {
    path: "/v1/personnametype",
    component: lazy(() => import("./pages/layer_type/PersonNameType")),
  },
  {
    path: "/v1/classifybyincome",
    component: lazy(() => import("./pages/layer_info/ClassifyByIncome")),
  },
  {
    path: "/v1/incomedetail/:paramId",
    component: lazy(() => import("./pages/layer_info/IncomeDetail")),
  },
  // { path: '/v1/legalorganization', component: lazy(() => import('./pages/layer_type/LegalOrganization')) },
  {
    path: "/v1/classifybyminority",
    component: lazy(() => import("./pages/layer_info/ClassifyByMinority")),
  },
  {
    path: "/v1/classifybyindustry",
    component: lazy(() => import("./pages/layer_info/ClassifyByIndustry")),
  },
  {
    path: "/v1/employeecountrange",
    component: lazy(() => import("./pages/layer_type/EmployeeCountRange")),
  },
  // { path: '/v1/informalorganization', component: lazy(() => import('./pages/layer_type/InformalOrganization')) },
  {
    path: "/v1/maritalstatustype",
    component: lazy(() => import("./pages/layer_type/MaritalStatusType")),
  },
  {
    path: "/v1/physicalcharacteristic",
    component: lazy(() => import("./pages/layer_info/PhysicalCharacteristic")),
  },
  {
    path: "/v1/physicalcharacteristictype",
    component: lazy(
      () => import("./pages/layer_type/PhysicalCharacteristicType")
    ),
  },

  {
    path: "/v1/gendertype",
    component: lazy(() => import("./pages/layer_type/Gendertype")),
  },
  {
    path: "/v1/team",
    component: lazy(() => import("./pages/layer_type/Team")),
  },
  {
    path: "/v1/family",
    component: lazy(() => import("./pages/layer_type/Family")),
  },
  {
    path: "/v1/otherinformalorganization",
    component: lazy(
      () => import("./pages/layer_type/OtherInformalOrganization")
    ),
  },

  {
    path: "/v1/governmentagency",
    component: lazy(() => import("./pages/layer_type/GovernmentAgency")),
  },
  {
    path: "/v1/corporation",
    component: lazy(() => import("./pages/layer_type/Corporation")),
  },
  {
    path: "/v1/persondetail",
    component: lazy(() => import("./pages/layer_info/PersonDetail")),
  },
  {
    path: "/v1/organizationmenu",
    component: lazy(() => import("./pages/layer_info/OrganizationMenu")),
  },
  {
    path: "/v1/person/:paramId",
    component: PersonDetail,
  },
  {
    path: "/v1/passportbycitizenshipid/:paramId",
    component: PassportByCitizenshipId,
  },
  {
    path: "/v1/eeocbypersonid/:paramId",
    component: lazy(() => import("./pages/layer_info/EeocByPersonId")),
  },
  {
    path: "/v1/eeocdetail/:paramId",
    component: lazy(() => import("./pages/layer_info/EeocDetail")),
  },
  {
    path: "/v1/incomebypersonid/:paramId",
    component: lazy(() => import("./pages/layer_info/IncomeByPersonId")),
  },
  {
    path: "/v1/organization",
    component: lazy(() => import("./pages/layer_type/Organization")),
  },
  {
    path: "/v1/organization/:param",
    component: lazy(() => import("./pages/layer_type/Organization")),
  },
  {
    path: "/v1/corporation/:paramId",
    component: lazy(() => import("./pages/layer_type/CorporationDetail")),
  },
  {
    path: "/v1/governmentagency/:paramId",
    component: lazy(() => import("./pages/layer_type/GovernmentAgencyDetail")),
  },
  {
    path: "/v1/family/:paramId",
    component: lazy(() => import("./pages/layer_type/FamilyDetail")),
  },
  {
    path: "/v1/otherinformalorganization/:paramId",
    component: lazy(
      () => import("./pages/layer_type/OtherInformalOrganizationDetail")
    ),
  },
  {
    path: "/v1/team/:paramId",
    component: lazy(() => import("./pages/layer_type/TeamDetail")),
  },
  {
    path: "/v1/organization/create",
    component: lazy(() => import("./pages/layer_type/OrganizationCreate")),
  },
  {
    path: "/v1/industrydetail/:paramId",
    component: lazy(() => import("./pages/layer_info/IndustryDetail")),
  },
  {
    path: "/v1/minoritydetail/:paramId",
    component: lazy(() => import("./pages/layer_info/MinorityDetail")),
  },
  {
    path: "/v1/sizedetail/:paramId",
    component: lazy(() => import("./pages/layer_info/SizeDetail")),
  },
  {
    path: "/v1/communicationeventpurposetype",
    component: lazy(() => import("./pages/layer_type/CommunicationEventPurposeType")),
  },
  {
    path: "/v1/contactmechanismtype",
    component: lazy(() => import("./pages/layer_type/ContactMechanismType")),
  },
  {
    path: "/v1/communicationeventstatustype",
    component: lazy(() => import("./pages/layer_type/CommunicationEventStatusType")),
  },
  {
    path: "/v1/prioritytype",
    component: lazy(() => import("./pages/layer_type/PriorityType")),
  },
  {
    path: "/v1/partyrelationshipstatustype",
    component: lazy(() => import("./pages/layer_type/PartyRelationshipStatusType")),
  },
  {
    path: "/v1/partyrelationshiptype",
    component: lazy(() => import("./pages/layer_type/PartyRelationshipType")),
  },
  {
    path: "/v1/roletype",
    component: lazy(() => import("./pages/layer_type/RoleType")),
  },
  {
    path: "/v1/partyrole",
    component: lazy(() => import("./pages/layer_role/PartyRole")),
  },
  {
    path: "/v1/partyrole/:paramId",
    component: lazy(() => import("./pages/layer_role/PartyRoleDetail")),
  },
  {
    path: "/v1/partyrelationship/",
    component: lazy(() => import("./pages/layer_relationship/PartyRelationship")),
  },
  {
    path: "/v1/partyrelationship/:paramId",
    component: lazy(() => import("./pages/layer_relationship/PartyRelationshipDetail")),
  },
  {
    path: "/v1/communicationevent/",
    component: lazy(() => import("./pages/layer_commu_event/CommunicationEvent")),
  },
  {
    path: "/v1/communicationevent/:paramId",
    component: lazy(() => import("./pages/layer_commu_event/CommunicationEventDetail")),
  },
  {
    path: "/v1/communicationeventpurpose/",
    component: lazy(() => import("./pages/layer_commu_purpose/CommunicationEventPurpose")),
  },
  {
    path: "/v1/communicationeventpurpose/:paramId",
    component: lazy(() => import("./pages/layer_commu_purpose/CommunicationEventPurposeDetail")),
  },
];

// สร้าง root element และ render แอปพลิเคชัน
createRoot(document.getElementById("root")!).render(
  // StrictMode ช่วยตรวจจับปัญหาในโค้ด เช่น deprecated APIs หรือ side effects
  <React.StrictMode>
    {/* ThemeProvider จัดการ theme ของ MUI สำหรับสีและสไตล์ทั่วแอป */}
    <ThemeProvider>
      {/* AuthProvider จัดการ state การ authentication เช่น isAuthenticated และ login/logout */}
      <AuthProvider>
        {/* BrowserRouter เปิดใช้งาน client-side routing */}
        <BrowserRouter>
          {/* Suspense แสดง Loading component ขณะ lazy load pages */}
          <Suspense fallback={<Loading />}>
            {/* Routes กำหนดเส้นทางทั้งหมดของแอป */}
            <Routes>
              {/* เส้นทางสำหรับหน้า Login และ Register ไม่ต้อง login */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* เส้นทางสำหรับหน้า Home ต้อง login โดยใช้ ProtectedRoute */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <Home />
                  </ProtectedRoute>
                }
              />

              {/* แมปรายการ routes อื่น ๆ ซึ่งต้อง login ทั้งหมด */}
              {routes.map((route) => (
                <Route
                  key={route.path}
                  path={route.path}
                  element={
                    <ProtectedRoute>
                      <route.component />
                    </ProtectedRoute>
                  }
                />
              ))}

              {/* เส้นทางสำหรับหน้า 404 เมื่อ URL ไม่ตรงกับ route ใด ๆ */}
              <Route path="*" element={<h1>404 Not Found</h1>} />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  </React.StrictMode>
);
