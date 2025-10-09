#include <SFML/Graphics.hpp>
#include <functional> 
#include <cmath> 
#include <iostream>


// Функция для отрисовки графика
void drawGraph(sf::RenderWindow& window, std::function<float(float)> func, float xMin, float xMax, float scaleX, float scaleY, sf::Color color) {
    sf::VertexArray graph(sf::LinesStrip);

    for (float x = xMin; x <= xMax; x += 0.1f) {
        float y = func(x); // Вычисление значения функции

        // Преобразование координат в экранные
        float screenX = 400 + x * scaleX;
        float screenY = 300 - y * scaleY;

        // Добавление точки в массив вершин
        graph.append(sf::Vertex(sf::Vector2f(screenX, screenY), color));
    }

    window.draw(graph);
}

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Graph Visualaiser");

    sf::CircleShape userPoint(5);
    userPoint.setFillColor(sf::Color::Red);
    bool userPointExists = false;

    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        return -1;
    }

    sf::Text coordinatesText;
    coordinatesText.setFont(font);
    coordinatesText.setCharacterSize(30);
    coordinatesText.setFillColor(sf::Color::White);
    coordinatesText.setPosition(10, 10);

    sf::Text messageText;
    messageText.setFont(font);
    messageText.setCharacterSize(30);
    messageText.setFillColor(sf::Color::White);
    messageText.setPosition(10, 40);

    // Оси X и Y
    sf::VertexArray xAxis(sf::Lines, 2);
    xAxis[0].position = sf::Vector2f(50, 300); // Начало оси X
    xAxis[0].color = sf::Color::White; // Цвет оси
    xAxis[1].position = sf::Vector2f(750, 300); // Конец оси X
    xAxis[1].color = sf::Color::White;

    sf::VertexArray yAxis(sf::Lines, 2);
    yAxis[0].position = sf::Vector2f(400, 50); // Начало оси Y
    yAxis[0].color = sf::Color::White; // Цвет оси
    yAxis[1].position = sf::Vector2f(400, 550); // Конец оси Y
    yAxis[1].color = sf::Color::White;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();

            // Проверка клика мышью
            if (event.type == sf::Event::MouseButtonPressed) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    // Получение позиции клика
                    sf::Vector2i mousePos = sf::Mouse::getPosition(window);

                    // Преобразование экранных координат в "математические"
                    float mathX = (mousePos.x - 400) / 10.0f; // Масштаб 3\10 по X
                    float mathY = -(mousePos.y - 300) / 10.0f; // Масштаб 10 по Y

                    // Установка новой пользовательской точки
                    userPoint.setPosition(mousePos.x - userPoint.getRadius(), mousePos.y - userPoint.getRadius());
                    userPointExists = true; // Помечаем, что точка существует

                    if ((abs(mathX) > mathY) and (mathY < 3)) {
                        messageText.setString("5");
                    }

                    if ((-3 < mathX < 3) and (abs(mathX) < mathY) and (mathY < 3)) {
                        messageText.setString("1");
                    }

                    if ((-3 < mathX < 3) and (abs(mathX) < mathY) and (mathY > 3)) {
                        messageText.setString("2");
                    }

                    if ((mathX < -3) and (abs(mathX) > mathY) and (mathY > 3)) {
                        messageText.setString("3");
                    }

                    if ((mathX > 3) and (abs(mathX) > mathY) and (mathY > 3)) {
                        messageText.setString("4");
                    }

                    if ((mathY == 3) or (abs(mathX) == mathY)) {
                        messageText.setString("On line");
                    }

                    // Обновление текста с координатами точки 
                    coordinatesText.setString("Coordinates: (" + std::to_string(mathX) + ", " + std::to_string(mathY) + ")");
                }
            }
        }


        window.clear();


        // Отрисовка осей
        window.draw(xAxis);
        window.draw(yAxis);




        drawGraph(window, [](float x) { return 3; }, -10, 10, 30, 10, sf::Color::Blue);

        drawGraph(window, [](float x) { return abs(x); }, -20, 20, 10, 10, sf::Color::Red);

        // Отрисовка пользовательской точки, если она существует
        if (userPointExists) {
            window.draw(userPoint);
            window.draw(coordinatesText);
            window.draw(messageText);
        }

        // Отображение нового кадра
        window.display();
    }
    std::cin.get();
    return 0;
}