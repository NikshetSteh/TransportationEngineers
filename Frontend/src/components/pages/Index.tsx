import background from "../../assets/background.png";
import Header from "../Header.tsx";

const HeroSection = () => (
    <section
        className="position-relative text-white"
        style={{height: "100vh"}}
    >
        {/* Background Image */}
        <img
            src={background}
            alt="Высокоскоростные поезда"
            className="position-absolute top-0 start-0 w-100 h-100 object-fit-cover"
        />

        {/* Adjusted Text Position */}
        <div
            className="position-absolute d-flex flex-column justify-content-center text-center"
            style={{
                top: "18%", // Position the div at 18% from the top
                left: "50%", // Center horizontally
                transform: "translateX(-50%)", // Adjust for horizontal centering
            }}
        >
            <h1 className="display-1 base-background p-1 m-0">Будущее транспорта</h1>
            <h2
                className="display-4"
                style={{marginTop: "1rem"}} // Add space between h1 and h2
            >
                Скорость. Инновации. Комфорт.
            </h2>
        </div>
    </section>
);

// Info Block Component
const InfoBlock = ({title, description}: { title: string; description: string }) => (
    <section className="py-5 text-center">
        <h2 className="fs-2 fw-bold mb-3">{title}</h2>
        <p
            className="fs-5 mx-auto info-block"
            style={{maxWidth: "600px", margin: "0 auto"}}
        >
            {description}
        </p>
    </section>
);

// Footer Component
const Footer = () => (
    <footer className="py-3 bg-secondary text-white text-center mt-auto">
        <p className="mb-1">© 2025 Высокоскоростные железные дороги</p>
        <ul className="list-unstyled">
            <li>
                <a href="#" className="text-white text-decoration-none">
                    Политика конфиденциальности
                </a>
            </li>
            <li>
                <a href="#" className="text-white text-decoration-none">
                    Пользовательское соглашение
                </a>
            </li>
        </ul>
    </footer>
);

// Main IndexPage Component
const Index = () => {
    return (
        <div className="d-flex flex-column min-vh-100">
            {/* Header */}
            <Header/>

            {/* Hero Section */}
            <HeroSection/>

            {/* Info Blocks */}
            <InfoBlock
                title="Высокоскоростные поезда будущего"
                description="Мы предлагаем инновационные высокоскоростные перевозки между городами, используя передовые технологии: искусственный интеллект для обеспечения безопасности, биометрическую идентификацию вместо билетов и контролёров, а также цифровые сервисы для удобства пассажиров."
            />
            <InfoBlock
                title="Искусственный интеллект"
                description="Автоматический контроль и анализ безопасности с применением ИИ."
            />
            <InfoBlock
                title="Биометрическая система"
                description="Больше никаких билетов! Вход на поезд с помощью биометрии."
            />

            {/* Footer */}
            <Footer/>
        </div>
    );
};

export default Index;