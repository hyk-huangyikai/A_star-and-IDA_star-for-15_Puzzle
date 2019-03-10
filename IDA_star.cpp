#pragma GCC optimize(2)
#include <iostream>
#include <queue>
#include <stack>
#include <time.h>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cstdio>

using namespace std;
const int ARRAY_SIZE = 4;

int movement[4][2] = {{1,0},{0,1},{-1,0},{0,-1}};
int target[16][2] = {{3,3},{0,0},{0,1},{0,2},{0,3},
					{1,0},{1,1},{1,2},{1,3},
					{2,0},{2,1},{2,2},{2,3},
					{3,0},{3,1},{3,2} };
int array1[ARRAY_SIZE][ARRAY_SIZE];

int is_target = 0;
int level;
int min_step;
vector <int> road;


int manhadun(int array1[ARRAY_SIZE][ARRAY_SIZE]) {
	int hn = 0,x,y;
	for (int i=0;i < ARRAY_SIZE;i++) {
		for (int j=0;j < ARRAY_SIZE;j++) {
			if (array1[i][j] != 0) {
				x = target[array1[i][j]][0];
				y = target[array1[i][j]][1];
				hn += abs(i - x) + abs(j - y);
			}
		}
	}
	return hn;
}

int chebyshev_distance(int array1[ARRAY_SIZE][ARRAY_SIZE]) {
	int hn = 0,x,y;
	for (int i=0;i < ARRAY_SIZE;i++) {
		for (int j=0;j < ARRAY_SIZE;j++) {
			if (array1[i][j] != 0) {
				x = target[array1[i][j]][0];
				y = target[array1[i][j]][1];
				int max1 = abs(i - x) > abs(j - y) ? abs(i - x) : abs(j - y);
				hn += max1;
			}
		}
	}
	return hn;
}

int right_element(int array1[ARRAY_SIZE][ARRAY_SIZE]) {
	int hn = 0,x,y;
	for (int i=0;i < ARRAY_SIZE;i++) {
		for (int j=0;j < ARRAY_SIZE;j++) {
			if (array1[i][j] != 0) {
				x = target[array1[i][j]][0];
				y = target[array1[i][j]][1];
				if (x != i or y != j) {
					hn += 1;
				}		
			}
		}
	}
	return hn;
}

int right_value(int array1[ARRAY_SIZE][ARRAY_SIZE]) {
	int hn = 0,x,y;
	int value;
	for (int i=0;i < ARRAY_SIZE;i++) {
		for (int j=0;j < ARRAY_SIZE;j++) {
			if (array1[i][j] != 0) {
				value = i*4 + j + 1;
				hn += abs(array1[i][j] - value);
			}
		}
	}
	return hn;
}


void my_swap(int *a,int *b) {
	int temp = *a;
	*a = *b;
	*b = temp;
}

void DFS( int gn,int back,int x_pos,int y_pos) {
	int hn = manhadun(array1);
//	int hn = chebyshev_distance(array1);
//	int hn = right_element(array1);
//	int hn = right_value(array1);
	if (is_target) {
		return ;
	}
	if (hn == 0) {
		is_target = 1;
		min_step = gn;
		return ;
	}
	for (int i=0;i < 4;++i) {
		int x = x_pos + movement[i][0];
		int y = y_pos + movement[i][1];
		if (x < 0 || x >= 4 || y < 0 || y >= 4) {
			continue;
		}
		if (back == -5 || i != (back+2) % 4) {
			road.push_back(array1[x][y]);
			my_swap(&array1[x][y],&array1[x_pos][y_pos]);
			hn = manhadun(array1);
//			hn = chebyshev_distance(array1);
//			hn = right_element(array1);
//			hn = right_value(array1);
			if (gn+hn <= level) {
				DFS(gn+1,i,x,y);
				if (is_target == 1) {
					return;
				}
			}
			my_swap(&array1[x][y],&array1[x_pos][y_pos]);
			road.pop_back();
		}
	}
}

void IDA(int x_pos,int y_pos) {
	level = manhadun(array1);
//	level = chebyshev_distance(array1);
//	level = right_element(array1);
//	level = right_value(array1);
	while (level <= 100 && is_target == 0) {
//		printf("%d\n",level);
		road.clear();
		DFS(0,-5,x_pos,y_pos);
		if (is_target) {
			break;
		}
		level += 2;
//		printf("%d\n",level); 
	}
}


int main () {
	time_t start = clock();
	ifstream fin ("input4.txt");
	int x_pos,y_pos;
	for (int i=0;i < ARRAY_SIZE;++i) {
		for (int j=0;j < ARRAY_SIZE;++j) {
			fin >> array1[i][j];
			if (array1[i][j] == 0) {
				x_pos = i;
				y_pos = j;
			}
		}
	}

	IDA(x_pos,y_pos);

	if (is_target) {
		printf("min step: %d\n",min_step);
		printf("load :\n");
		for (int i=0;i < road.size();++i) {
			printf("%d ",road[i]);
		}
		printf("\n");
	}
	else {
		printf("No Way!!!\n");
	}
	
	time_t end = clock();

	printf("run time:  %.6lf s\n" ,(double)(end - start) / 1000 );


	return 0;
}
