import { StrictMode, Suspense, lazy } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Loading from "./components/Loading";

// global variable theme ของทั้งเว็บ
import { ThemeProvider } from "./contexts/ThemeContext";

// Lazy load Home page
// โหลดหน้า Home แบบ Lazy
const Home = lazy(() => import("./pages/Home"));

// กำหนด array ของ routes พร้อม path และ component
// Define an array of routes with path and component
const routes = [
  { path: "/users", component: lazy(() => import("./pages/Users")) },
  {
    path: "/v1/maritalstatustype",
    component: lazy(() => import("./pages/MaritalStatusType")),
  },
  {
    path: "/v1/personnametype",
    component: lazy(() => import("./pages/PersonNameType")),
  },
  {
    path: "/v1/physicalcharacteristictype",
    component: lazy(() => import("./pages/PhysicalCharacteristicType")),
  },
  { path: "/v1/country", component: lazy(() => import("./pages/Country")) },
  {
    path: "/v1/maritalstatus",
    component: lazy(() => import("./pages/MaritalStatus")),
  },
  {
    path: "/v1/personname",
    component: lazy(() => import("./pages/PersonName")),
  },
  {
    path: "/v1/citizenship",
    component: lazy(() => import("./pages/Citizenship")),
  },
  { path: "/v1/passport", component: lazy(() => import("./pages/Passport")) },
  { path: "/v1/person", component: lazy(() => import("./pages/Person")) },
  { path: "/v1/partytype", component: lazy(() => import("./pages/PartyType")) },
  {
    path: "/v1/partyclassification",
    component: lazy(() => import("./pages/PartyClassification")),
  },
  {
    path: "/v1/legalorganization",
    component: lazy(() => import("./pages/LegalOrganization")),
  },
  {
    path: "/v1/physicalcharacteristic",
    component: lazy(() => import("./pages/PhysicalCharacteristic")),
  },
  {
    path: "/v1/informalorganization",
    component: lazy(() => import("./pages/InformalOrganization")),
  },
  { path: "/v1/ethnicity", component: lazy(() => import("./pages/Ethnicity")) },
  {
    path: "/v1/incomerange",
    component: lazy(() => import("./pages/IncomeRange")),
  },
  {
    path: "/v1/industrytype",
    component: lazy(() => import("./pages/IndustryType")),
  },
  {
    path: "/v1/employeecountrange",
    component: lazy(() => import("./pages/EmployeeCountRange")),
  },
  {
    path: "/v1/minoritytype",
    component: lazy(() => import("./pages/MinorityType")),
  },
  {
    path: "/v1/classifybyeeoc",
    component: lazy(() => import("./pages/ClassifyByEEOC")),
  },
  {
    path: "/v1/classifybyincome",
    component: lazy(() => import("./pages/ClassifyByIncome")),
  },
  {
    path: "/v1/classifybyindustry",
    component: lazy(() => import("./pages/ClassifyByIndustry")),
  },
  {
    path: "/v1/classifybysize",
    component: lazy(() => import("./pages/ClassifyBySize")),
  },
  {
    path: "/v1/classifybyminority",
    component: lazy(() => import("./pages/ClassifyByMinority")),
  },
];

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <BrowserRouter>
        <Suspense fallback={<Loading />}>
          <Routes>
            {/* หน้า Home */}
            {/* Home page */}
            <Route path="/" element={<Home />} />

            {/* ใช้ map เพื่อสร้าง Route จาก array */}
            {/* Use map to generate Routes from the array */}
            {routes.map((route) => (
              <Route
                key={route.path}
                path={route.path}
                element={<route.component />}
              />
            ))}

            {/* หน้า 404 สำหรับ path ที่ไม่ match */}
            {/* 404 page for unmatched paths */}
            <Route path="*" element={<h1>404 Not Found</h1>} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </ThemeProvider>
  </StrictMode>
);
