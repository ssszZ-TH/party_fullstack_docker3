import React, { lazy, Suspense } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import ProtectedRoute from './components/ProtectedRoute';
import Loading from './components/Loading';

// Lazy load pages เพื่อเพิ่มประสิทธิภาพโดยโหลดเฉพาะหน้าเมื่อจำเป็น
const Home = lazy(() => import('./pages/Home'));
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));

// กำหนด array ของ routes สำหรับหน้าเพิ่มเติม
// แต่ละ route มี path และ component ที่ lazy load
// เรียงลำดับตามความยาวของ path จากสั้นไปยาวเพื่อความสวยงามและอ่านง่าย
const routes = [
  { path: '/vite', component: lazy(() => import('./App')) },
  { path: '/users', component: lazy(() => import('./pages/Users')) },
  { path: '/v1/person', component: lazy(() => import('./pages/Person')) },
  { path: '/v1/country', component: lazy(() => import('./pages/Country')) },
  { path: '/v1/passport', component: lazy(() => import('./pages/Passport')) },
  { path: '/v1/profile', component: lazy(() => import('./pages/Profile')) },
  { path: '/v1/partytype', component: lazy(() => import('./pages/PartyType')) },
  { path: '/v1/ethnicity', component: lazy(() => import('./pages/Ethnicity')) },
  { path: '/v1/personname', component: lazy(() => import('./pages/PersonName')) },
  { path: '/v1/incomerange', component: lazy(() => import('./pages/IncomeRange')) },
  { path: '/v1/citizenship', component: lazy(() => import('./pages/Citizenship')) },
  { path: '/v1/industrytype', component: lazy(() => import('./pages/IndustryType')) },
  { path: '/v1/minoritytype', component: lazy(() => import('./pages/MinorityType')) },
  { path: '/v1/maritalstatus', component: lazy(() => import('./pages/MaritalStatus')) },
  { path: '/v1/classifybyeeoc', component: lazy(() => import('./pages/ClassifyByEEOC')) },
  { path: '/v1/classifybysize', component: lazy(() => import('./pages/ClassifyBySize')) },
  { path: '/v1/personnametype', component: lazy(() => import('./pages/PersonNameType')) },
  { path: '/v1/classifybyincome', component: lazy(() => import('./pages/ClassifyByIncome')) },
  { path: '/v1/legalorganization', component: lazy(() => import('./pages/LegalOrganization')) },
  { path: '/v1/classifybyminority', component: lazy(() => import('./pages/ClassifyByMinority')) },
  { path: '/v1/classifybyindustry', component: lazy(() => import('./pages/ClassifyByIndustry')) },
  { path: '/v1/employeecountrange', component: lazy(() => import('./pages/EmployeeCountRange')) },
  { path: '/v1/informalorganization', component: lazy(() => import('./pages/InformalOrganization')) },
  { path: '/v1/maritalstatustype', component: lazy(() => import('./pages/MaritalStatusType')) },
  { path: '/v1/physicalcharacteristic', component: lazy(() => import('./pages/PhysicalCharacteristic')) },
  { path: '/v1/physicalcharacteristictype', component: lazy(() => import('./pages/PhysicalCharacteristicType')) },
];

// สร้าง root element และ render แอปพลิเคชัน
createRoot(document.getElementById('root')!).render(
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