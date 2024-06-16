interface ISiteMetadataResult {
  siteTitle: string;
  siteUrl: string;
  description: string;
  keywords: string;
  logo: string;
  navLinks: {
    name: string;
    url: string;
  }[];
}

const data: ISiteMetadataResult = {
  siteTitle: 'Workouts Map',
  siteUrl: 'https://tangultra.github.io/workouts_page/',
  logo: 'https://raw.githubusercontent.com/cuijianzhuang/picx-images-hosting/master/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20240616220617.7p3gjjhany.webp',
  description: 'Personal site and blog',
  keywords: 'workouts, running, cycling, riding, roadtrip, hiking, swimming',
  navLinks: [
    {
      name: 'Blog',
      url: 'https://tangultra.github.io/workouts_page/',
    },
    {
      name: 'About',
      url: 'https://tangultra.github.io/workouts_page/',
    },
  ],
};

export default data;
