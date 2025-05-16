import React, { lazy, Suspense, useContext } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthContext, AuthProvider } from "./contexts/AuthContext";
import Loading from "./components/Loading";
import { ThemeProvider } from "./contexts/ThemeContext";

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

// Lazy load pages
const Home = lazy(() => import("./pages/Home"));
const Login = lazy(() => import("./pages/Login"));
const Register = lazy(() => import("./pages/Register"));

// กำหนด array ของ routes
const routes = [
  { path: "/vite", component: lazy(() => import("./App")) },
  { path: "/users", component: lazy(() => import("./pages/Users")) },
  { path: "/v1/maritalstatustype", component: lazy(() => import("./pages/MaritalStatusType")) },
  { path: "/v1/personnametype", component: lazy(() => import("./pages/PersonNameType")) },
  { path: "/v1/physicalcharacteristictype", component: lazy(() => import("./pages/PhysicalCharacteristicType")) },
  { path: "/v1/country", component: lazy(() => import("./pages/Country")) },
  { path: "/v1/maritalstatus", component: lazy(() => import("./pages/MaritalStatus")) },
  { path: "/v1/personname", component: lazy(() => import("./pages/PersonName")) },
  { path: "/v1/citizenship", component: lazy(() => import("./pages/Citizenship")) },
  { path: "/v1/passport", component: lazy(() => import("./pages/Passport")) },
  { path: "/v1/person", component: lazy(() => import("./pages/Person")) },
  { path: "/v1/partytype", component: lazy(() => import("./pages/PartyType")) },
  { path: "/v1/partyclassification", component: lazy(() => import("./pages/PartyClassification")) },
  { path: "/v1/legalorganization", component: lazy(() => import("./pages/LegalOrganization")) },
  { path: "/v1/physicalcharacteristic", component: lazy(() => import("./pages/PhysicalCharacteristic")) },
  { path: "/v1/informalorganization", component: lazy(() => import("./pages/InformalOrganization")) },
  { path: "/v1/ethnicity", component: lazy(() => import("./pages/Ethnicity")) },
  { path: "/v1/incomerange", component: lazy(() => import("./pages/IncomeRange")) },
  { path: "/v1/industrytype", component: lazy(() => import("./pages/IndustryType")) },
  { path: "/v1/employeecountrange", component: lazy(() => import("./pages/EmployeeCountRange")) },
  { path: "/v1/minoritytype", component: lazy(() => import("./pages/MinorityType")) },
  { path: "/v1/classifybyeeoc", component: lazy(() => import("./pages/ClassifyByEEOC")) },
  { path: "/v1/classifybyincome", component: lazy(() => import("./pages/ClassifyByIncome")) },
  { path: "/v1/classifybyindustry", component: lazy(() => import("./pages/ClassifyByIndustry")) },
  { path: "/v1/classifybysize", component: lazy(() => import("./pages/ClassifyBySize")) },
  { path: "/v1/classifybyminority", component: lazy(() => import("./pages/ClassifyByMinority")) },
  { path: "/v1/profile", component: lazy(() => import("./pages/Profile")) },
];

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Suspense fallback={<Loading />}>
            <Routes>
              {/* หน้า Login และ Register */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* หน้า Home และ routes อื่นๆ ที่ต้อง login */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <Home />
                  </ProtectedRoute>
                }
              />
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

              {/* หน้า 404 */}
              <Route path="*" element={<h1>404 Not Found</h1>} />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  </React.StrictMode>
);