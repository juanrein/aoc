use std::fs;
use std::collections::{HashMap, VecDeque, HashSet};
use std::cmp;

fn neighbors(grid: &Vec<Vec<String>>, pos: (i64,i64), n: i64, m: i64) -> Vec<(i64, i64)>{
    let (i,j) = pos;
    let mut res = Vec::new();
    for (ni,nj) in [(i+1, j), (i-1,j), (i,j-1), (i, j+1)] {
        if ni >= 0 && nj >= 0 && ni < n && nj < m {
            if grid[ni as usize][nj as usize] != "#" {
                res.push((ni,nj));
            }
        }
    }
    res
}

fn next_connection(g: &HashMap<(i64, i64), HashSet<(i64, i64)>>, current: &(i64,i64), prev: &(i64, i64)) -> Option<(i64, i64)>{
    match g.get(current) {
        None => None,
        Some(adjacents) => {
            let next: HashSet<(i64, i64)> = adjacents.iter().filter(|x| *x != prev).map(|x| x.clone()).collect();
            if next.len() == 1 {
                match next.iter().nth(0) {
                    None => None,
                    Some(x) => Some(x.clone())
                }
            }
            else {
                None
            }
        }    
    }
}

// combine one way paths into one long jump and format grid into adjacency list
fn simplify(grid: &Vec<Vec<String>>, n: i64, m: i64) -> HashMap<(i64, i64),HashSet<((i64, i64), i64)>> {
    let mut g: HashMap<(i64, i64), HashSet<(i64, i64)>> = HashMap::new();

    for i in 0..n {
        for j in 0..m {
            if grid[i as usize][j as usize] != "#" {
                for n in neighbors(&grid, (i,j), n, m) {
                    g.entry((i,j)).or_default().insert(n);
                }
            }
        }
    }

    let mut gg: HashMap<(i64, i64), HashSet<((i64, i64), i64)>> = HashMap::new();

    for (u,destinations) in g.iter() {
        for v in destinations.iter() {
            let mut w = 1;
            let mut prev = u.clone();
            let mut current = v.clone();
            while next_connection(&g, &current, &prev).is_some() {
                let next = next_connection(&g, &current, &prev).unwrap();
                prev = current;
                current = next;
                w += 1;

            }
            gg.entry(u.clone()).or_default().insert((current, w));
        }
    }

    gg
}

fn traverse(graph: &HashMap<(i64, i64),HashSet<((i64, i64), i64)>>, start: (i64, i64), end: (i64, i64)) -> i64 {
    let mut q: VecDeque<((i64, i64), HashSet<(i64, i64)>, i64)> = VecDeque::new();
    q.push_back((start, HashSet::new(), 0));
    let mut best = 0;

    while q.len() > 0 {
        let (pos, visited, d) = q.pop_front().unwrap();
        if pos == end {
            best = cmp::max(best, d);
            continue;   
        }
        for (next_pos, w) in graph.get(&pos).unwrap().iter() {
            if visited.contains(next_pos) {
                continue;
            }
            let mut visited_clone = visited.clone();
            visited_clone.insert(pos);
            q.push_back((next_pos.clone(), visited_clone, d + w));
        } 
    }

    best
}

fn main() {
    let grid: Vec<Vec<String>> = 
        fs::read_to_string("input.txt")
        .expect("not read")
        .lines()
        .map(String::from)
        .map(|s| s.chars().map(|c| c.to_string()).collect())
        .collect();
    
    let start: (i64, i64) = (0,1);
    let n: i64 = grid.len().try_into().unwrap();
    let m: i64 = grid[0].len().try_into().unwrap();
    let end: (i64, i64) = (n-1, m-2);

    let graph = simplify(&grid, n, m);

    let res = traverse(&graph, start, end);

    println!("{res}")
}
