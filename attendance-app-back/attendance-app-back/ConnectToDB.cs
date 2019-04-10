using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace attendance_app_back
{
    class ConnectToDB
    {
        static void Main(string[] args)
        {
            string connetionString = null;
            SqlConnection cnn;
            connetionString = "Server = localhost; Database = AttendanceApp_db; Integrated Security = SSPI; ";
            cnn = new SqlConnection(connetionString);
            try
            {
                cnn.Open();
                Console.WriteLine("Connection Open ! ");
                cnn.Close();
            }
            catch (Exception ex)
            {
                Console.WriteLine("Can not open connection ! ");
            }
        }
    }
}
