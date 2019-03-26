using System;
using System.Text;
using LibUsbDotNet;
using LibUsbDotNet.Main;

namespace RFIDReader_2._0
{
    internal class ReadPolling
    {
        public static UsbDevice MyUsbDevice;

        public static UsbDeviceFinder MyUsbFinder = new UsbDeviceFinder(0x058F);

        public static void Main(string[] args)
        {
            ErrorCode ec = ErrorCode.None;

            try
            {
                MyUsbDevice = UsbDevice.OpenUsbDevice(MyUsbFinder);

                if (MyUsbDevice == null) throw new Exception("Device Not Found.");
                
                IUsbDevice wholeUsbDevice = MyUsbDevice as IUsbDevice;
                if (!ReferenceEquals(wholeUsbDevice, null))
                {
                    wholeUsbDevice.SetConfiguration(1);
                    wholeUsbDevice.ClaimInterface(0);
                }

                UsbEndpointReader reader = MyUsbDevice.OpenEndpointReader(ReadEndpointID.Ep01);


                byte[] readBuffer = new byte[1024];
                while (ec == ErrorCode.None)
                {
                    int bytesRead;

                    ec = reader.Read(readBuffer, 60000, out bytesRead);

                    if (bytesRead == 0) throw new Exception(string.Format("{0}:No more bytes!", ec));
                    Console.Write("{0} bytes read - ", bytesRead);

                    Console.Write(Encoding.Default.GetString(readBuffer, 0, bytesRead));
                    Console.WriteLine();
                }

                Console.WriteLine("\r\nDone!\r\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine();
                Console.WriteLine((ec != ErrorCode.None ? ec + ":" : String.Empty) + ex.Message);
            }
            finally
            {
                if (MyUsbDevice != null)
                {
                    if (MyUsbDevice.IsOpen)
                    {
                        IUsbDevice wholeUsbDevice = MyUsbDevice as IUsbDevice;
                        if (!ReferenceEquals(wholeUsbDevice, null))
                        {
                            wholeUsbDevice.ReleaseInterface(0);
                        }

                        MyUsbDevice.Close();
                    }
                    MyUsbDevice = null;

                    UsbDevice.Exit();

                }

                Console.ReadKey();
            }
        }
    }
}