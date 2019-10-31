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
        Move bestMove = findBestMove();
        board.makeMove(bestMove, player);
        return bestMove;
    }

    private Move findBestMove() throws InvalidMoveError {
        Move best = null;
        int alpha = Integer.MIN_VALUE;
        int beta = Integer.MAX_VALUE;
        Vector<Vector<Move>> moves = board.getAllPossibleMoves(player);
         for (Vector<Move> moveVector : moves) {
             for (Move value : moveVector) {
                 int score = Minimax(1, value, ((player == 1) ? 2 : 1), alpha, beta);
                 if (score > alpha) {
                     alpha = score;
                     best = value;
                 }
             }
         }
         return best;
    }

    private int Minimax(int d, Move move, int p, int alpha, int beta) throws InvalidMoveError{
        board.makeMove(move, p);
        if(d == 3){
            //return Evaluate(move);
               int k;
               k = board.blackCount - board.whiteCount;
               board.Undo();
               return k;
            }
        Vector<Vector<Move>> moves = board.getAllPossibleMoves(p);
        if(moves.isEmpty()){
            board.Undo();
            return Evaluate(move);
        }
        if(p == 1){
            int best = Integer.MIN_VALUE;
            for (Vector<Move> moveVector : moves) {
                for (Move value : moveVector) {
                    int score = Minimax((d + 1), value, ((p == 1) ? 2 : 1), alpha, beta);
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
            board.Undo();
            return best;
        }else{
            int best = Integer.MAX_VALUE;
            for (Vector<Move> moveVector : moves) {
                for (Move value : moveVector) {
                    int score = Minimax((d + 1), value, ((p == 1) ? 2 : 1), alpha, beta);
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
            board.Undo();
            return best;
        }

    }

    private int Evaluate(Move move){
         return 0;
    }
}
