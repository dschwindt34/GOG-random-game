using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Data.SQLite;
using System.Collections.Specialized;
using Dapper;
using GOGRandomGameLibrary;

namespace GOGRandomGame
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            WindowStartupLocation = WindowStartupLocation.CenterScreen;
        }

        private void OkayButton_Click(object sender, RoutedEventArgs e)
        {
            DataAccess dbInstance = new DataAccess();
            List<string> selection = new List<string>();
            selection = dbInstance.GetRandomResult();
            Result_Window reswin = new Result_Window(selection[0], selection[1], selection[2]);
            reswin.Show();

        }

        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.Shutdown();
        }
    }
}
