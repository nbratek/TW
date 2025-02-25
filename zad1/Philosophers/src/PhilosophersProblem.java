import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.concurrent.Semaphore;

public class PhilosophersProblem {

    public enum Solution {
        NAIWNE,
        ZAGLODZENIE,
        ASYMETRYCZNE,
        STOCHASTYCZNE,
        ARBITER,
        JADALNIA
    }

    public static void main(String[] args) {
        int numberOfPhilosophers = 5;
        Solution solution = Solution.JADALNIA; // Zmiana na wybrany wariant
        Philosopher[] philosophers = new Philosopher[numberOfPhilosophers];
        Object[] forks = new Object[numberOfPhilosophers];


        for (int i = 0; i < numberOfPhilosophers; i++) {
            forks[i] = new Object();
        }

        Semaphore lokaj = null;
        if (solution == Solution.ARBITER || solution == Solution.JADALNIA) {
            lokaj = new Semaphore(numberOfPhilosophers - 1);
        }


        for (int i = 0; i < numberOfPhilosophers; i++) {
            Object leftFork = forks[i];
            Object rightFork = forks[(i + 1) % numberOfPhilosophers];

            switch (solution) {
                case NAIWNE:
                    philosophers[i] = new NaivePhilosopher(i, leftFork, rightFork);
                    break;
                case ZAGLODZENIE:
                    philosophers[i] = new StarvationPhilosopher(i, leftFork, rightFork);
                    break;
                case ASYMETRYCZNE:
                    if (i % 2 == 0) {
                        philosophers[i] = new AsymmetricPhilosopher(i, rightFork, leftFork);
                    } else {
                        philosophers[i] = new AsymmetricPhilosopher(i, leftFork, rightFork);
                    }
                    break;
                case STOCHASTYCZNE:
                    philosophers[i] = new StochasticPhilospher(i, leftFork, rightFork);
                    break;
                case ARBITER:
                    philosophers[i] = new ArbiterPhilosopher(i, leftFork, rightFork, lokaj);
                    break;
                case JADALNIA:
                    philosophers[i] = new DiningRoomPhilospher(i, leftFork, rightFork, lokaj, numberOfPhilosophers);
                    break;
            }

            new Thread(philosophers[i], "Filozof " + (i + 1)).start();
        }


        try {
            Thread.sleep(10000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }


        for (Philosopher philosopher : philosophers) {
            philosopher.stopRunning();
        }


        for (Philosopher philosopher : philosophers) {
            System.out.println("Filozof " + (philosopher.getId() + 1) + " średni czas oczekiwania: "
                    + philosopher.getAverageWaitingTime() + " ms");
        }
        double[] averageWaitingTimes = new double[numberOfPhilosophers];
        for (int i = 0; i < numberOfPhilosophers; i++) {
            philosophers[i].stopRunning();
            averageWaitingTimes[i] = philosophers[i].getAverageWaitingTime();

        }

        //saveToCSV("data/wyniki_stochastyczne_n15.csv", averageWaitingTimes);
    }


    public static void saveToCSV(String path, double[] data) {
        try (FileWriter writer = new FileWriter(path, true)) {
            StringBuilder sb = new StringBuilder();
            for (double wartosc : data) {
                sb.append(wartosc).append(",");
            }
            sb.deleteCharAt(sb.length() - 1);
            sb.append("\n");
            writer.write(sb.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


abstract class Philosopher implements Runnable {

    protected int id;
    protected Object leftFork;
    protected Object rightFork;
    protected volatile boolean works = true;

    protected long totalWaitingTime = 0;
    protected int numberOfMeals = 0;

    public Philosopher(int id, Object leftFork, Object rightFork) {
        this.id = id;
        this.leftFork = leftFork;
        this.rightFork = rightFork;
    }

    protected void think() throws InterruptedException {
        // System.out.println("Filozof " + (id + 1) + " myśli.");
        Thread.sleep((long) (Math.random() * 100));
    }

    protected void eat() throws InterruptedException {
        // System.out.println("Filozof " + (id + 1) + " je.");
        Thread.sleep((long) (Math.random() * 100));
    }

    public void stopRunning() {
        works = false;
    }

    public int getId() {
        return id;
    }

    public double getAverageWaitingTime() {
        return numberOfMeals > 0 ? (double) totalWaitingTime / numberOfMeals : 0;
    }
}

// 1. Rozwiązanie naiwne (z możliwością blokady)
class NaivePhilosopher extends Philosopher {

    public NaivePhilosopher(int id, Object leftFork, Object rightFork) {
        super(id, leftFork, rightFork);
    }

    @Override
    public void run() {
        try {
            while (works) {
                think();
                long start = System.currentTimeMillis();
                synchronized (leftFork) {
                    System.out.println("Filozof " + (id + 1) + " podniósł lewy widelec.");
                    synchronized (rightFork) {
                        long end = System.currentTimeMillis();
                        totalWaitingTime += (end - start);
                        numberOfMeals++;
                        System.out.println("Filozof " + (id + 1) + " podniósł prawy widelec.");
                        eat();
                    }
                    System.out.println("Filozof " + (id + 1) + " odłożył prawy widelec.");
                }
                System.out.println("Filozof " + (id + 1) + " odłożył lewy widelec.");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
    }
}

// 2. Rozwiązanie z możliwością zagłodzenia
class StarvationPhilosopher extends Philosopher {

    public StarvationPhilosopher(int id, Object leftFork, Object rightFork) {
        super(id, leftFork, rightFork);
    }

    @Override
    public void run() {
        try {
            while (works) {
                think();
                long start = System.currentTimeMillis();


                boolean leftAvailable = false;
                boolean rightAvailable = false;

                synchronized (leftFork) {
                    leftAvailable = true;
                    synchronized (rightFork) {
                        rightAvailable = true;
                        long end = System.currentTimeMillis();
                        totalWaitingTime += (end - start);
                        numberOfMeals++;
                        eat();
                    }
                }


                if (!leftAvailable || !rightAvailable) {
                    Thread.sleep((long) (Math.random() * 100));
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
    }
}

// 3. Rozwiązanie asymetryczne
class AsymmetricPhilosopher extends Philosopher {

    public AsymmetricPhilosopher(int id, Object leftFork, Object rightFork) {
        super(id, leftFork, rightFork);
    }

    @Override
    public void run() {
        try {
            while (works) {
                think();
                long start = System.currentTimeMillis();
                synchronized (leftFork) {
                    synchronized (rightFork) {
                        long end = System.currentTimeMillis();
                        totalWaitingTime += (end - start);
                        numberOfMeals++;
                        eat();
                    }
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
    }
}

// 4. Rozwiązanie stochastyczne
class StochasticPhilospher extends Philosopher {

    public StochasticPhilospher(int id, Object leftFork, Object righFork) {
        super(id, leftFork, righFork);
    }

    @Override
    public void run() {
        Random random = new Random();
        try {
            while (works) {
                think();
                boolean leftFirst = random.nextBoolean();
                long start = System.currentTimeMillis();
                if (leftFirst) {
                    synchronized (leftFork) {
                        synchronized (rightFork) {
                            long end = System.currentTimeMillis();
                            totalWaitingTime += (end - start);
                            numberOfMeals++;
                            eat();
                        }
                    }
                } else {
                    synchronized (rightFork) {
                        synchronized (leftFork) {
                            long end = System.currentTimeMillis();
                            totalWaitingTime += (end - start);
                            numberOfMeals++;
                            eat();
                        }
                    }
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
    }
}

// 5. Rozwiązanie z arbitrem (lokajem)
class ArbiterPhilosopher extends Philosopher {

    private Semaphore lokaj;

    public ArbiterPhilosopher(int id, Object leftFork, Object rightFork, Semaphore lokaj) {
        super(id, leftFork, rightFork);
        this.lokaj = lokaj;
    }

    @Override
    public void run() {
        try {
            while (works) {
                think();
                lokaj.acquire();
                long start = System.currentTimeMillis();
                synchronized (leftFork) {
                    synchronized (rightFork) {
                        long end = System.currentTimeMillis();
                        totalWaitingTime += (end - start);
                        numberOfMeals++;
                        eat();
                    }
                }
                lokaj.release();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
    }
}

// 6. Rozwiązanie z jadalnią
class DiningRoomPhilospher extends Philosopher {

    private Semaphore lokaj;
    private int liczbaFilozofow;

    public DiningRoomPhilospher(int id, Object leftFork, Object rightFork, Semaphore lokaj, int liczbaFilozofow) {
        super(id, leftFork, rightFork);
        this.lokaj = lokaj;
        this.liczbaFilozofow = liczbaFilozofow;
    }

    @Override
    public void run() {
        try {
            while (works) {
                think();
                boolean wJadalni = lokaj.tryAcquire();
                long start = System.currentTimeMillis();

                if (wJadalni) {
                    synchronized (leftFork) {
                        synchronized (rightFork) {
                            long end = System.currentTimeMillis();
                            totalWaitingTime += (end - start);
                            numberOfMeals++;
                            eat();
                        }
                    }
                    lokaj.release();
                } else {
                    synchronized (rightFork) {
                        synchronized (leftFork) {
                            long end = System.currentTimeMillis();
                            totalWaitingTime += (end - start);
                            numberOfMeals++;
                            eat();
                        }
                    }
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
    }
}
