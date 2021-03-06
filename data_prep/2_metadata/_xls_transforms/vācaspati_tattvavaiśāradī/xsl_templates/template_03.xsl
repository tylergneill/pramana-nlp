<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
 <xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
 </xsl:copy>
</xsl:template>

<xsl:template match="//p">
<p>
<xsl:copy-of select="./@*"/>
<xsl:attribute name="locus">
<xsl:value-of select="parent::div/@n"/>.<xsl:number count="p"/>
</xsl:attribute>
<xsl:copy-of select="./text()"/>
</p>
</xsl:template>

</xsl:stylesheet>