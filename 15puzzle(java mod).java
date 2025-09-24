package org.kentrugithud.puzzle15;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.GridLayout;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.Random;

public class MainActivity extends AppCompatActivity {
    private Button[][] tiles = new Button[4][4];
    private int emptyRow = 3, emptyCol = 3;
    private int moveCount = 0;
    private TextView moveTextView;
    private GridLayout gridLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initializeGame();
        setupTiles();
        shuffleTiles();
    }

    private void initializeGame() {
        moveTextView = findViewById(R.id.moveTextView);
        gridLayout = findViewById(R.id.gridLayout);

        Button shuffleButton = findViewById(R.id.shuffleButton);
        Button githubButton = findViewById(R.id.githubButton);

        shuffleButton.setOnClickListener(v -> shuffleTiles());
        githubButton.setOnClickListener(v -> showGithubMessage());
    }

    private void setupTiles() {
        for (int row = 0; row < 4; row++) {
            for (int col = 0; col < 4; col++) {
                tiles[row][col] = new Button(this);
                tiles[row][col].setTextSize(20);
                tiles[row][col].setTextColor(Color.WHITE);

                // Сохраняем позицию плитки
                final int currentRow = row;
                final int currentCol = col;

                tiles[row][col].setOnClickListener(v -> moveTile(currentRow, currentCol));

                // Настройка размера и расположения
                GridLayout.Spec rowSpec = GridLayout.spec(row, 1f);
                GridLayout.Spec colSpec = GridLayout.spec(col, 1f);
                GridLayout.LayoutParams params = new GridLayout.LayoutParams(rowSpec, colSpec);
                params.width = 0;
                params.height = 0;
                params.setMargins(8, 8, 8, 8);

                gridLayout.addView(tiles[row][col], params);
            }
        }
    }

    private void moveTile(int row, int col) {
        // Проверяем, можно ли переместить плитку
        if ((Math.abs(row - emptyRow) == 1 && col == emptyCol) ||
                (Math.abs(col - emptyCol) == 1 && row == emptyRow)) {

            // Меняем плитки местами
            tiles[emptyRow][emptyCol].setText(tiles[row][col].getText());
            tiles[emptyRow][emptyCol].setBackgroundColor(Color.parseColor("#6495ED"));
            tiles[row][col].setText("");
            tiles[row][col].setBackgroundColor(Color.parseColor("#333333"));

            // Обновляем позицию пустой плитки
            emptyRow = row;
            emptyCol = col;

            // Счетчик ходов
            moveCount++;
            moveTextView.setText("Ходы: " + moveCount);

            // Проверяем победу
            checkWin();
        }
    }

    private void shuffleTiles() {
        moveCount = 0;
        moveTextView.setText("Ходы: 0");

        // Заполняем поле числами
        int number = 1;
        for (int row = 0; row < 4; row++) {
            for (int col = 0; col < 4; col++) {
                if (number < 16) {
                    tiles[row][col].setText(String.valueOf(number));
                    tiles[row][col].setBackgroundColor(Color.parseColor("#6495ED"));
                } else {
                    tiles[row][col].setText("");
                    tiles[row][col].setBackgroundColor(Color.parseColor("#333333"));
                    emptyRow = row;
                    emptyCol = col;
                }
                number++;
            }
        }

        // Делаем случайные ходы для перемешивания
        Random random = new Random();
        for (int i = 0; i < 1000; i++) {
            int direction = random.nextInt(4);
            int newRow = emptyRow;
            int newCol = emptyCol;

            switch (direction) {
                case 0: // Вверх
                    newRow--;
                    break;
                case 1: // Вниз
                    newRow++;
                    break;
                case 2: // Влево
                    newCol--;
                    break;
                case 3: // Вправо
                    newCol++;
                    break;
            }

            // Проверяем границы и перемещаем
            if (newRow >= 0 && newRow < 4 && newCol >= 0 && newCol < 4) {
                // Временно сохраняем текст для перемещения
                String tempText = tiles[newRow][newCol].getText().toString();
                tiles[emptyRow][emptyCol].setText(tempText);
                tiles[emptyRow][emptyCol].setBackgroundColor(Color.parseColor("#6495ED"));
                tiles[newRow][newCol].setText("");
                tiles[newRow][newCol].setBackgroundColor(Color.parseColor("#333333"));

                emptyRow = newRow;
                emptyCol = newCol;
            }
        }
    }

    private void checkWin() {
        int expectedNumber = 1;

        for (int row = 0; row < 4; row++) {
            for (int col = 0; col < 4; col++) {
                // Последняя клетка должна быть пустой
                if (row == 3 && col == 3) {
                    if (!tiles[row][col].getText().toString().isEmpty()) {
                        return; // Не победа
                    }
                } else {
                    String tileText = tiles[row][col].getText().toString();
                    if (tileText.isEmpty() || Integer.parseInt(tileText) != expectedNumber) {
                        return; // Не победа
                    }
                }
                expectedNumber++;
            }
        }

        // Победа!
        Toast.makeText(this, "Поздравляем! Вы решили головоломку за " + moveCount + " ходов!",
                Toast.LENGTH_LONG).show();
    }

    private void showGithubMessage() {
        Toast.makeText(this, "GitHub: https://github.com/kentrugithud/15-puzzle-",
                Toast.LENGTH_SHORT).show();
    }
}