import { createBrowserRouter } from "react-router-dom"
import { Root } from "./routes/root"
import { ErrorPage } from "./error-page"
import { HomeScreen } from "./routes"
import { SignUp } from "./routes/sign-up"
import { SignIn } from "./routes/sign-in"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <HomeScreen /> },
      {
        path: "sign-up",
        element: <SignUp />,
      },
      {
        path: "sign-in",
        element: <SignIn />
      }
    ]
  },
])
