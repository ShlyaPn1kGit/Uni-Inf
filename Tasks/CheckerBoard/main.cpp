#include <SFML/Graphics.hpp>
#include <SFML/System.hpp> 
#include <SFML/Window.hpp> 
#include <iostream>
using namespace sf;

int main()
{
	RenderWindow window(VideoMode({500, 500 }), "CheckerBoard");

	window.clear();

	const int cellSize = 50;
	const int gridSize = 10;
	
	RectangleShape cells[gridSize][gridSize];
	for (int i = 0; i < gridSize; i++) {
		for (int j = 0; j < gridSize; j++) {
			cells[i][j].setSize(Vector2f{ cellSize - 2, cellSize - 2 });
			cells[i][j].setPosition(i * cellSize, j * cellSize);
			cells[i][j].setOutlineColor(Color::Black);
			if ((i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0)) {
				cells[i][j].setFillColor(Color::Green);
			}
			else {
				cells[i][j].setFillColor(Color::White);
			}
			cells[i][j].setOutlineThickness(1);
		}
	}

	while (window.isOpen()) {
		Event event;
		while (window.pollEvent(event)) {
			if (event.type == Event::Closed) {
				window.close();
			}
		}
			
			window.clear(Color::White);

			for (int i = 0; i < gridSize; i++) {
				for (int j = 0; j < gridSize; j++) {
					window.draw(cells[i][j]);
				}
			}

			window.display();
	}


}
