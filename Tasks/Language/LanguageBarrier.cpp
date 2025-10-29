#include <iostream>
#include <string>
#include <windows.h>
#include <cmath>
using namespace std;


void findArrayWithMaxNegative(const int* arrA, const int* arrB, int size) {
    int countA = 0, countB = 0;

    for (int i = 0; i < size; i++) {
        if (arrA[i] < 0) {
            countA++;
        }

    }

    for (int i = 0; i < size; i++) {
        if (arrB[i] < 0) {
            countB++;
        }

    }

    if (countA > countB) {
        cout << "Элементы массива A: ";
        for (int i = 0; i < size; i++) {
            cout << arrA[i] << " ";
        }
        cout << "Элементы массива B: ";
        for (int i = 0; i < size; i++) {
            cout << arrB[i] << " ";
        }
    }
    else {
        cout << "Элементы массива B: ";
        for (int i = 0; i < size; i++) {
            cout << arrB[i] << " ";
        }
        cout << "Элементы массива A: ";
        for (int i = 0; i < size; i++) {
            cout << arrA[i] << " ";
        }
    }
}

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    int N; // Размер массивов

    // Ввод размера массивов
    cout << "Введите размер массивов (N): ";
    cin >> N;

    int* A = new int[N]; // Динамическое выделение памяти для массива A
    int* B = new int[N]; // Динамическое выделение памяти для массива B

    // Ввод массивов
    cout << "Введите " << N << " элементов для массива A:" << endl;
    for (int i = 0; i < N; i++) {
        cin >> A[i];
    }

    cout << "Введите " << N << " элементов для массива B:" << endl;
    for (int i = 0; i < N; i++) {
        cin >> B[i];
    }

    // Поиск массива с наибольшей суммой
    findArrayWithMaxNegative(A, B, N);

    // Освобождение выделенной памяти
    delete[] A;
    delete[] B;

    return 0;
}