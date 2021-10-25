using Dapper;
using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Linq;

namespace GOGRandomGameLibrary
{
    public class DataAccess
    {
        public List<string> GetRandomResult()
        {
            Random rnd = new Random();
            List<string> result = new List<string>();
            List<string> titles = GetTitles();
            List<string> urls = GetImageUrls();

            int i = rnd.Next(titles.Count);
            result.Insert(0, titles[i]);
            result.Insert(1, TrimUrl(urls[i]));
            result.Insert(2, titles.Count.ToString());
            return result;
            
        }
        public List<string> GetTitles()
        {
            using (SQLiteConnection conn = new SQLiteConnection(@"Data Source = C:\ProgramData\GOG.com\Galaxy\storage\galaxy-2.0.db;"))
            {
                var output = conn.Query<string>(@"SELECT trim(trim(GamePieces.value,'{ ""title"":""'),'""}')
                                                  FROM GamePieces
                                                  WHERE gamePieceTypeId = 42
                                                  AND releaseKey NOT LIKE '%generic%'");
                return output.ToList();
                //Random rnd = new Random();
                //return titles[rnd.Next(titles.Count)];
            }
        }

        public List<string> GetImageUrls()
        {
            using (SQLiteConnection conn = new SQLiteConnection(@"Data Source = C:\ProgramData\GOG.com\Galaxy\storage\galaxy-2.0.db;"))
            {
                var output = conn.Query<string>(@"SELECT GamePieces.value
                                                  FROM GamePieces
                                                  WHERE gamePieceTypeId = 40
                                                  AND releaseKey NOT LIKE '%generic%'");
                return output.ToList();
            }
        }
        public string TrimUrl(string url)
        {
            string[] parts = url.Split('"');
            string rawUrl = parts[parts.Length - 2];
            return rawUrl.Replace("\\", "");
        }
    }
}
