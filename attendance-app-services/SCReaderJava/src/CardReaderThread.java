import javax.smartcardio.*;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.sql.*;
import com.microsoft.sqlserver.jdbc.*;

public class CardReaderThread implements Runnable {

    public static AtomicBoolean running;
    public static void setRunning(AtomicBoolean running) {
        CardReaderThread.running = running;
    }
    @Override
    public void run() {
        running = new AtomicBoolean(Boolean.TRUE);
        try {
            //Class.forName("com.microsoft.sqlserver.jdbc");
            String connectionUrl = "jdbc:sqlserver://localhost:1433;databaseName=AttendanceApp_db";
            String user = "SA"; //login
            String password = "WartaPoznan1912!"; //hasło
            Connection con = DriverManager.getConnection(connectionUrl, user, password);

            TerminalFactory factory = TerminalFactory.getDefault();
            List<CardTerminal> terminals = factory.terminals().list();
            System.out.println("Terminals: " + terminals);

            CardTerminal reader = terminals.get(0);

            System.out.println("Listening...");

            while (running.get()) {
                while (!reader.isCardPresent()) {
                    if (!running.get()) {
                        return;
                    }
                }

                Card card = reader.connect("*");
                card.beginExclusive();
                CardChannel channel = card.getBasicChannel();
                ResponseAPDU resp = channel.transmit(new CommandAPDU(128, 202, 0x9f, 0x7f, 256));
                byte[] data = resp.getData();
                byte[] ICSerialNumber = Arrays.copyOfRange(data, 15, 19);

                System.out.println(hexToString(ICSerialNumber));
                //podaj pełną ścieżkę do tabeli (database.schema.table)
                String queryCheck = "UPDATE AttendanceApp_db.dbo.Obecnosci SET isPresent = 1 WHERE nr_legitymacji = \'" + hexToString(ICSerialNumber) + "\'";
                Statement st = con.createStatement();
                st.executeUpdate(queryCheck);
//                while(rs.next())
//                {
//                    System.out.print(rs.getString(1)); //or rs.getString("column name");
//                }

                //hexToString(ICSerialNumber) to nasz numer karty

                while (reader.isCardPresent()) {
                    if (!running.get()) {
                        return;
                    }
                }
            }

        } catch (CardException e) {
            e.printStackTrace();
        } //catch (SQLException e) {
        catch (SQLException e) {
            e.printStackTrace();
        }
        //e.printStackTrace();
        //}
    }

    private String hexToString(final byte[] data) {
        char[] hexValue = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
        int length = data.length;
        char[] out = new char[length*2];
        for (int i = 0, j = 0; i < length; i++) {
            out[j++] = hexValue[(0xF0 & data[i]) >>> 4];
            out[j++] = hexValue[0x0F & data[i]];
        }
        return new String(out);
    }
}
