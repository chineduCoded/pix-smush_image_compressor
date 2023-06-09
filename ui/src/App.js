import MainContent from "./components/MainContent";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer"
import MenuBar from "./components/Menubar";

function App() {
  return (
    <div>
      <Navbar />
      <MainContent>
        <MenuBar />
      </MainContent>
      <Footer />
    </div>
  );
}

export default App;
