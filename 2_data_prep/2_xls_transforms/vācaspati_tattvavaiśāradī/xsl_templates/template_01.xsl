<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
 <xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
 </xsl:copy>
</xsl:template>

<xsl:template match="teiHeader" />

<xsl:template match="head[@lang='en']" />

<xsl:template match="head/supplied"><xsl:value-of select="."/></xsl:template>

<xsl:template match="label"/>

<xsl:template match="comment()"/>

<xsl:template match="pb"/>

<xsl:template match="ref">(<xsl:value-of select="."/>)</xsl:template>

</xsl:stylesheet>

