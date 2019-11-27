import java.util.Random;
import java.util.Vector;

// The following part should be completed by students.
// Students can modify anything except the class name and exisiting functions and varibles.

public class StudentAI extends AI {
    public StudentAI(int col, int row, int k) throws InvalidParameterError {
        super(col, row, k);

        this.board = new Board(col, row, k);
        this.board.initializeGame();
        this.player = 2;
    }

    public Move GetMove(Move move) throws InvalidMoveError {
        if (!move.seq.isEmpty())
            board.makeMove(move, (player == 1) ? 2 : 1);
        else
            player = 1;
        //Vector<Vector<Move>> moves = board.getAllPossibleMoves(player);
        //Random randGen = new Random();
        //int index = randGen.nextInt(moves.size());
        //int innerIndex = randGen.nextInt(moves.get(index).size());
        //Move resMove = moves.get(index).get(innerIndex);
        //System.out.println("hi");
        Move bestMove = findBestMove();
        //System.out.println("hi");
        board.makeMove(bestMove, player);
        //System.out.println("hi");
        return bestMove;
    }

    private Move findBestMove() throws InvalidMoveError {
        Move best = null;
        double alpha = Integer.MIN_VALUE;
        double beta = Integer.MAX_VALUE;
        Vector<Vector<Move>> moves = board.getAllPossibleMoves(player);
        //System.out.println("moves: "+moves.toString());
         for (Vector<Move> moveVector : moves) {
             for (Move value : moveVector) {
                 //System.out.println("move: " + value.toString());
                 board.makeMove(value, player);
                 double score = Minimax(1, value, ((player == 1) ? 2 : 1), alpha, beta);
                 board.Undo();
                 if (score > alpha) {
                     alpha = score;
                     best = value;
                     //System.out.println("move :" + best + " n :" + alpha);
                 }
             }
         }
         //System.out.println("move: " + best.toString());
         return best;
    }

    private double Minimax(int d, Move move, int p, double alpha, double beta) throws InvalidMoveError{
        //board.makeMove(move, p);
        if(d == 5){
            //return Evaluate(move)
                double score = 0;
                score = Evaluate();
                return score;
            }
        Vector<Vector<Move>> moves = board.getAllPossibleMoves(p);
        if(moves.size() == 0){
            double score = 0;
            score = Evaluate();
            return score;
        }
        if(p == player){
            //System.out.println("hi");
            double best = Double.MIN_VALUE;
            for (Vector<Move> moveVector : moves) {
                for (Move value : moveVector) {
                    board.makeMove(value, p);
                    double score = Minimax((d + 1), value, ((player == 1) ? 2 : 1), alpha, beta);
                    board.Undo();
                    if (score > best) {
                        best = score;
                    }
                    if (best > alpha) {
                        alpha = best;
                    }
                    //pruning
                    if (alpha >= beta) {
                        break;
                    }
                }
            }
            //System.out.println("n = " + best);
            return best;
        }else{
            double best = Double.MAX_VALUE;
            for (Vector<Move> moveVector : moves) {
                for (Move value : moveVector) {
                    board.makeMove(value, p);
                    double score = Minimax((d + 1), value, player, alpha, beta);
                    board.Undo();
                    if (score < best) {
                        best = score;
                    }
                    if (best < beta) {
                        beta = best;
                    }
                    //pruning
                    if (alpha >= beta) {
                        break;
                    }
                }
            }
            return best;
        }

    }

    private double Evaluate(){
        double k = 0;
        int wKing = 0;
        int bKing = 0;
        if(player == 1) {
            k = (board.blackCount - board.whiteCount);
            for(Vector<Checker> checkerVector : board.board){
                for(Checker checker : checkerVector){
                    if(checker.color == "B"){
                        if(checker.col == board.col - 1 || checker.col == 0){
                            //System.out.println(checker.col);
                            k += 0.3;
                        }
                        if(board.isInBoard(checker.row -1, checker.col -1)){
                            for(Vector<Checker> m : board.board){
                                for(Checker n : checkerVector) {
                                    if( n.row == checker.row - 1 && n.col == checker.col - 1){
                                        if(n.color == "B") {
                                            k += 0.1;
                                        }
                                    }
                                }
                            }
                        }
                        if(board.isInBoard(checker.row +1, checker.col -1)){
                            for(Vector<Checker> m : board.board){
                                for(Checker n : checkerVector) {
                                    if( n.row == checker.row + 1 && n.col == checker.col - 1){
                                        if(n.color == "B") {
                                            k += 0.1;
                                        }
                                    }
                                }
                            }
                        }
                        if(board.isInBoard(checker.row -1, checker.col +1)){
                            for(Vector<Checker> m : board.board){
                                for(Checker n : checkerVector) {
                                    if( n.row == checker.row - 1 && n.col == checker.col + 1){
                                        if(n.color == "B") {
                                            k += 0.1;
                                        }
                                    }
                                }
                            }
                        }
                        if(board.isInBoard(checker.row +1, checker.col +1)){
                            for(Vector<Checker> m : board.board){
                                for(Checker n : checkerVector) {
                                    if( n.row == checker.row + 1 && n.col == checker.col + 1){
                                        if(n.color == "B") {
                                            k += 0.1;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    if(checker.isKing == true){
                        if(checker.color == "W"){
                            wKing++;
                        }
                        if(checker.color == "B"){
                            bKing++;
                        }
                    }
                }
            }
            k += (bKing - wKing) * 0.5;
        }else{
            k = (board.whiteCount - board.blackCount);
            for(Vector<Checker> checkerVector : board.board){
                for(Checker checker : checkerVector){
                    if(checker.color == "W"){
                        if(checker.col == board.col - 1 || checker.col == 0){
                            //System.out.println(checker.col);
                            k += 0.3;
                        }
                        if(board.isInBoard(checker.row -1, checker.col -1)){
                            for(Vector<Checker> m : board.board){
                                for(Checker n : checkerVector) {
                                    if( n.row == checker.row - 1 && n.col == checker.col - 1){
                                        if(n.color == "W") {
                                            k += 0.1;
                                        }
                                    }
                                }
                            }
                        }
                        if(board.isInBoard(checker.row +1, checker.col -1)){
                            for(Vector<Checker> m : board.board){
                                for(Checker n : checkerVector) {
                                    if( n.row == checker.row + 1 && n.col == checker.col - 1){
                                        if(n.color == "W") {
                                            k += 0.1;
                                        }
                                    }
                                }
                            }
                        }
                        if(board.isInBoard(checker.row -1, checker.col +1)){
                            for(Vector<Checker> m : board.board){
                                for(Checker n : checkerVector) {
                                    if( n.row == checker.row - 1 && n.col == checker.col + 1){
                                        if(n.color == "W") {
                                            k += 0.1;
                                        }
                                    }
                                }
                            }
                        }
                        if(board.isInBoard(checker.row +1, checker.col +1)){
                            for(Vector<Checker> m : board.board){
                                for(Checker n : checkerVector) {
                                    if( n.row == checker.row + 1 && n.col == checker.col + 1){
                                        if(n.color == "W") {
                                            k += 0.1;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    if(checker.isKing == true){
                        if(checker.color == "W"){
                            wKing++;
                        }
                        if(checker.color == "B"){
                            bKing++;
                        }
                    }
                }
            }
            k += (wKing - bKing) * 0.5;
        }
         return k;
    }

}
